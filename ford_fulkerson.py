import os
import json
import csv
import networkx as nx
from collections import defaultdict

# Répertoires
RESULTATS_DIR = "resultats"
INSTANCES_DIR = "instances"
FORD_FULKERSON_DIR = os.path.join(RESULTATS_DIR, "ford_fulkerson")

# Les 10 algorithmes à tester
ALGOS = ["EFT", "HRPW*", "HRU1", "HRU2", "LFT", "LST", "MTS", "STFD", "TIMRES", "TIMROS"]

# Durées fixes des activités (à adapter à ton problème)
durations = [
    3, 2, 4, 3, 2, 1, 2, 4, 1, 2, 1, 3,
    2, 3, 2, 1, 2, 3, 1, 2, 3, 2
]

def build_resource_constraint_graph(ordered_activities, durations, num_resources=1):
    """
    Construit un graphe de flot pour modéliser les contraintes de ressources.
    Chaque activité nécessite une ressource pendant sa durée d'exécution.
    """
    G = nx.DiGraph()
    source = "source"
    sink = "sink"
    
    # Calcul des temps de début et de fin pour chaque activité
    start_times = {}
    end_times = {}
    current_time = 0
    
    for i, act in enumerate(ordered_activities):
        duration = durations[act - 1]
        start_times[act] = current_time
        end_times[act] = current_time + duration
        current_time += duration
    
    # Création des nœuds temporels
    all_times = set()
    for act in ordered_activities:
        all_times.add(start_times[act])
        all_times.add(end_times[act])
    all_times = sorted(all_times)
    
    # Ajout de la source et du sink
    G.add_node(source)
    G.add_node(sink)
    
    # Pour chaque activité, créer des arcs
    for act in ordered_activities:
        activity_node = f"act_{act}"
        G.add_node(activity_node)
        
        # Arc de la source vers l'activité (capacité = 1)
        G.add_edge(source, activity_node, capacity=1)
        
        # Arc de l'activité vers le sink (capacité = 1)
        G.add_edge(activity_node, sink, capacity=1)
    
    return G, source, sink

def build_precedence_graph(ordered_activities, durations):
    """
    Construit un graphe de flot basé sur les contraintes de précédence.
    Le max flow représente le nombre maximum d'activités pouvant être exécutées.
    """
    G = nx.DiGraph()
    source = "source"
    sink = "sink"
    
    # Ajouter tous les nœuds d'activités
    for act in ordered_activities:
        G.add_node(f"act_{act}")
    
    # Connecter la source à toutes les activités
    for act in ordered_activities:
        G.add_edge(source, f"act_{act}", capacity=1)
    
    # Connecter toutes les activités au sink
    for act in ordered_activities:
        G.add_edge(f"act_{act}", sink, capacity=1)
    
    # Ajouter les contraintes de précédence basées sur l'ordre
    for i in range(len(ordered_activities) - 1):
        current_act = ordered_activities[i]
        next_act = ordered_activities[i + 1]
        # Pas de contrainte supplémentaire car l'ordre est déjà respecté
    
    return G, source, sink

def build_time_expanded_graph(ordered_activities, durations):
    """
    Construit un graphe temporel étendu pour modéliser l'utilisation des ressources dans le temps.
    """
    G = nx.DiGraph()
    source = "source"
    sink = "sink"
    
    # Calcul de la durée totale du projet
    total_duration = sum(durations[act - 1] for act in ordered_activities)
    
    # Création des nœuds de temps
    time_nodes = []
    for t in range(total_duration + 1):
        time_node = f"time_{t}"
        time_nodes.append(time_node)
        G.add_node(time_node)
    
    # Connexion entre nœuds de temps consécutifs (capacité = nombre de ressources)
    for t in range(total_duration):
        G.add_edge(f"time_{t}", f"time_{t+1}", capacity=1)
    
    # Ajout des activités
    current_time = 0
    for act in ordered_activities:
        duration = durations[act - 1]
        start_time = current_time
        end_time = current_time + duration
        
        activity_node = f"act_{act}"
        G.add_node(activity_node)
        
        # Connexion source -> activité
        G.add_edge(source, activity_node, capacity=1)
        
        # Connexion activité -> temps de début
        G.add_edge(activity_node, f"time_{start_time}", capacity=1)
        
        # Connexion temps de fin -> sink
        G.add_edge(f"time_{end_time}", sink, capacity=1)
        
        current_time = end_time
    
    return G, source, sink

def compute_max_flow_multiple_methods(ordered_activities, durations):
    """
    Calcule le max flow avec plusieurs méthodes pour validation croisée.
    Retourne les résultats et la valeur principale du max flow.
    """
    results = {}
    max_flow = 0  # Variable principale pour stocker le max flow
    
    # Méthode 1: Graphe simple de précédence
    try:
        G1, source1, sink1 = build_precedence_graph(ordered_activities, durations)
        flow1, _ = nx.maximum_flow(G1, source1, sink1, flow_func=nx.algorithms.flow.edmonds_karp)
        results['precedence'] = flow1
        max_flow = max(max_flow, flow1)  # Mise à jour du max flow
    except Exception as e:
        results['precedence'] = f"Erreur: {e}"
    
    # Méthode 2: Graphe de contraintes de ressources
    try:
        G2, source2, sink2 = build_resource_constraint_graph(ordered_activities, durations)
        flow2, _ = nx.maximum_flow(G2, source2, sink2, flow_func=nx.algorithms.flow.edmonds_karp)
        results['resource'] = flow2
        max_flow = max(max_flow, flow2)  # Mise à jour du max flow
    except Exception as e:
        results['resource'] = f"Erreur: {e}"
    
    # Méthode 3: Calcul direct basé sur la faisabilité
    try:
        # Pour un ordonnancement séquentiel, le max flow est le nombre d'activités
        # qui peuvent être effectivement exécutées
        feasible_activities = len([act for act in ordered_activities if act <= len(durations)])
        results['direct'] = feasible_activities
        max_flow = max(max_flow, feasible_activities)  # Mise à jour du max flow
    except Exception as e:
        results['direct'] = f"Erreur: {e}"
    
    return results, max_flow

def analyze_schedule_quality(ordered_activities, durations):
    """
    Analyse la qualité de l'ordonnancement en calculant différentes métriques.
    """
    metrics = {}
    
    # Durée totale du projet
    total_duration = sum(durations[act - 1] for act in ordered_activities if act <= len(durations))
    metrics['total_duration'] = total_duration
    
    # Nombre d'activités valides
    valid_activities = [act for act in ordered_activities if 1 <= act <= len(durations)]
    metrics['valid_activities'] = len(valid_activities)
    metrics['invalid_activities'] = len(ordered_activities) - len(valid_activities)
    
    # Utilisation des ressources (supposant 1 ressource)
    if total_duration > 0:
        metrics['resource_utilization'] = len(valid_activities) / total_duration
    else:
        metrics['resource_utilization'] = 0
    
    return metrics

def load_ordered_activities_from_json(filepath):
    """Charge les activités ordonnées depuis un fichier JSON."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data.get("ordered_activities", [])
    except Exception as e:
        print(f"Erreur lors du chargement de {filepath}: {e}")
        return []

def export_results_to_csv(all_instances_results, output_path):
    """
    Exporte les résultats de tous les algorithmes dans un fichier CSV pour comparaison.
    """
    headers = ["Instance", "Meilleur_Algorithme", "Flot_Maximal"] + ALGOS

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for instance_data in all_instances_results:
            instance = instance_data["instance"]
            best_algo = instance_data["best_algorithm"]
            best_flow = instance_data["best_max_flow"]
            results = instance_data["algorithms_results"]

            row = [instance, best_algo, best_flow]
            for algo in ALGOS:
                if algo in results:
                    max_flow_value = results[algo]["max_flow"]
                    row.append(max_flow_value)
                else:
                    row.append("N/A")
            writer.writerow(row)

    print(f"📊 Résultats exportés vers : {output_path}")

def export_detailed_csv(all_instances_results, output_path):
    """
    Exporte un CSV détaillé avec toutes les métriques pour analyse approfondie.
    """
    headers = ["Instance", "Algorithme", "Max_Flow", "Duree_Totale", 
               "Activites_Valides", "Activites_Invalides", "Utilisation_Ressources"]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        for instance_data in all_instances_results:
            instance = instance_data["instance"]
            results = instance_data["algorithms_results"]
            
            for algo in ALGOS:
                if algo in results:
                    data = results[algo]
                    row = [
                        instance,
                        algo,
                        data["max_flow"],
                        data["metrics"]["total_duration"],
                        data["metrics"]["valid_activities"],
                        data["metrics"]["invalid_activities"],
                        round(data["metrics"]["resource_utilization"], 4)
                    ]
                    writer.writerow(row)
    
    print(f"📋 Résultats détaillés exportés vers : {output_path}")

def load_dzn_instance(filepath):
    """
    Charge les durées d'activités depuis un fichier DZN.
    Retourne une liste de durées (int).
    """
    if not os.path.isfile(filepath):
        return []
    durations = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                # Recherche une ligne contenant 'duree' ou 'durations'
                if 'duree' in line or 'durations' in line:
                    # Extrait les nombres entre crochets ou accolades
                    import re
                    match = re.search(r'=\s*[\[\{]([^\]\}]*)[\]\}]', line)
                    if match:
                        values = match.group(1)
                        durations = [int(x) for x in values.replace(',', ' ').split()]
                        break
    except Exception as e:
        print(f"Erreur lors du chargement de {filepath}: {e}")
        return []
    return durations

def get_instances_from_dzn():
    """
    Retourne la liste des noms d'instances (sans extension) présents dans le dossier INSTANCES_DIR.
    """
    instances = []
    if not os.path.isdir(INSTANCES_DIR):
        return instances
    for filename in os.listdir(INSTANCES_DIR):
        if filename.endswith(".dzn"):
            instance_name = filename[:-4]  # Retire '.dzn'
            instances.append(instance_name)
    return instances

def main():
    """Fonction principale pour traiter toutes les instances."""
    os.makedirs(FORD_FULKERSON_DIR, exist_ok=True)

    # Détection des instances DZN
    dzn_instances = get_instances_from_dzn()
    print(f"🔍 Instances DZN détectées : {len(dzn_instances)}")
    if dzn_instances:
        print(f"  Instances trouvées : {', '.join(dzn_instances[:5])}{'...' if len(dzn_instances) > 5 else ''}")

    # Détection des instances avec résultats JSON
    instances_with_results = set()
    for algo in ALGOS:
        algo_dir = os.path.join(RESULTATS_DIR, algo)
        if not os.path.isdir(algo_dir):
            continue
        for filename in os.listdir(algo_dir):
            if filename.endswith(".json"):
                instance_name = filename[:-5]
                instances_with_results.add(instance_name)

    print(f"🔍 Instances avec résultats JSON : {len(instances_with_results)}")
    
    # Intersection des instances DZN et des résultats
    common_instances = set(dzn_instances) & instances_with_results
    print(f"🎯 Instances communes (DZN + résultats) : {len(common_instances)}")
    
    if not common_instances:
        print("⚠️ Aucune instance commune trouvée. Vérifiez les noms des fichiers.")
        # Affichage pour debugging
        print(f"Instances DZN : {dzn_instances[:3]}...")
        print(f"Instances JSON : {sorted(list(instances_with_results))[:3]}...")
        return
    
    # Stockage des résultats pour export CSV
    all_instances_results = []
    
    # Traitement de chaque instance
    for instance in sorted(common_instances):
        print(f"\n🧪 Traitement de l'instance : {instance}")
        
        # Chargement des durées depuis le fichier DZN
        dzn_filepath = os.path.join(INSTANCES_DIR, f"{instance}.dzn")
        instance_durations = load_dzn_instance(dzn_filepath)
        
        if not instance_durations:
            print(f"⚠️ Impossible de charger les durées pour {instance}, utilisation des durées par défaut")
            instance_durations = durations  # Utilise les durées par défaut
        else:
            print(f"✅ Durées chargées depuis {instance}.dzn : {len(instance_durations)} activités")
        
        results = {}
        
        for algo in ALGOS:
            filepath = os.path.join(RESULTATS_DIR, algo, f"{instance}.json")
            if not os.path.isfile(filepath):
                print(f"  ⚠️ Fichier manquant pour {algo}")
                continue
                
            ordered = load_ordered_activities_from_json(filepath)
            if not ordered:
                print(f"  ⚠️ Données vides pour {algo}")
                continue
            
            # Calcul des max flows avec les durées de l'instance
            max_flows, max_flow = compute_max_flow_multiple_methods(ordered, instance_durations)
            
            # Analyse de la qualité de l'ordonnancement
            metrics = analyze_schedule_quality(ordered, instance_durations)
            
            results[algo] = {
                "max_flow": max_flow,  # Variable principale du max flow
                "max_flows_details": max_flows,  # Détails par méthode
                "metrics": metrics,
                "ordered_activities": ordered
            }
            
            print(f"  {algo:8} → Max Flow = {max_flow}")
            print(f"          → Détails: {max_flows}")
            print(f"          → Métriques: durée={metrics['total_duration']}, "
                  f"activités_valides={metrics['valid_activities']}")

        if not results:
            print(f"⚠️ Aucune donnée pour l'instance {instance}.")
            continue

        # Analyse comparative - Utilisation de la variable max_flow principale
        best_algo = None
        best_max_flow = 0
        
        for algo, data in results.items():
            if data['max_flow'] > best_max_flow:
                best_max_flow = data['max_flow']
                best_algo = algo
        
        # Analyse détaillée par méthode
        comparison = {}
        for method in ['precedence', 'resource', 'direct']:
            method_results = {}
            for algo, data in results.items():
                if method in data['max_flows_details'] and isinstance(data['max_flows_details'][method], (int, float)):
                    method_results[algo] = data['max_flows_details'][method]
            
            if method_results:
                best_algo_method = max(method_results.items(), key=lambda x: x[1])[0]
                comparison[method] = {
                    "best_algorithm": best_algo_method,
                    "best_value": method_results[best_algo_method],
                    "all_values": method_results
                }

        # Sauvegarde des résultats
        summary = {
            "instance": instance,
            "best_algorithm": best_algo,
            "best_max_flow": best_max_flow,
            "algorithms_results": results,
            "comparison_by_method": comparison,
            "analysis_info": {
                "total_algorithms": len(results),
                "activity_duration_list": instance_durations,
                "dzn_file": f"{instance}.dzn"
            }
        }
        
        # Ajout aux résultats globaux pour CSV
        all_instances_results.append(summary)

        out_path = os.path.join(FORD_FULKERSON_DIR, f"{instance}.json")
        with open(out_path, 'w') as f_out:
            json.dump(summary, f_out, indent=2)

        print(f"✅ Résultats sauvegardés dans {out_path}")
        print(f"🏆 MEILLEUR ALGORITHME: {best_algo} avec MAX FLOW = {best_max_flow}")
        
        # Affichage du résumé détaillé
        for method, comp in comparison.items():
            print(f"📊 Méthode {method}: Meilleur = {comp['best_algorithm']} "
                  f"(valeur = {comp['best_value']})")
    
    # Export des résultats en CSV
    if all_instances_results:
        # CSV de comparaison principal
        csv_comparison_path = os.path.join(FORD_FULKERSON_DIR, "comparaison_algorithmes.csv")
        export_results_to_csv(all_instances_results, csv_comparison_path)
        
        # CSV détaillé
        csv_detailed_path = os.path.join(FORD_FULKERSON_DIR, "resultats_detailles.csv")
        export_detailed_csv(all_instances_results, csv_detailed_path)
        
        # Statistiques globales
        print(f"\n📈 STATISTIQUES GLOBALES:")
        print(f"  • Nombre total d'instances traitées: {len(all_instances_results)}")
        
        # Comptage des victoires par algorithme
        algo_wins = defaultdict(int)
        for result in all_instances_results:
            if result["best_algorithm"]:
                algo_wins[result["best_algorithm"]] += 1
        
        print(f"  • Victoires par algorithme:")
        for algo in sorted(algo_wins.keys()):
            print(f"    - {algo}: {algo_wins[algo]} victoires")
        
        # Algorithme le plus performant globalement
        if algo_wins:
            best_global_algo = max(algo_wins.items(), key=lambda x: x[1])
            print(f"  🥇 Algorithme le plus performant: {best_global_algo[0]} ({best_global_algo[1]} victoires)")
    
    else:
        print("⚠️ Aucune donnée à exporter.")

if __name__ == "__main__":
    main()