import os
import json
import csv
import re
import networkx as nx

# Répertoires
RESULTATS_DIR = "resultats"
INSTANCES_DIR = "instances"
FORD_FULKERSON_DIR = os.path.join(RESULTATS_DIR, "ford_fulkerson")

# Algorithmes à comparer
ALGOS = [
    "EFT", "HRPW*", "HRU1", "HRU2", "LFT",
    "LST", "MTS", "STFD", "TIMRES", "TIMROS"
]


def build_resource_constraint_graph(ordered_activities, durations):
    """Construit un graphe pour les contraintes de ressources"""
    G = nx.DiGraph()
    source, sink = "source", "sink"
    start_times, end_times = {}, {}
    current_time = 0

    for act in ordered_activities:
        if act <= len(durations):
            duration = durations[act - 1]
            start_times[act] = current_time
            end_times[act] = current_time + duration
            current_time += duration

    G.add_node(source)
    G.add_node(sink)

    for act in ordered_activities:
        if act <= len(durations):
            node = f"act_{act}"
            G.add_node(node)
            G.add_edge(source, node, capacity=1)
            G.add_edge(node, sink, capacity=1)

    return G, source, sink


def build_precedence_graph(ordered_activities, durations):
    """Construit un graphe de précédence"""
    G = nx.DiGraph()
    source, sink = "source", "sink"

    G.add_node(source)
    G.add_node(sink)

    for act in ordered_activities:
        if act <= len(durations):
            node = f"act_{act}"
            G.add_node(node)
            G.add_edge(source, node, capacity=1)
            G.add_edge(node, sink, capacity=1)

    return G, source, sink


def build_time_expanded_graph(ordered_activities, durations):
    """Construit un graphe temporel étendu"""
    G = nx.DiGraph()
    source, sink = "source", "sink"

    valid_activities = [act for act in ordered_activities if act <= len(durations)]
    if not valid_activities:
        return G, source, sink

    total_duration = sum(durations[act - 1] for act in valid_activities)

    G.add_node(source)
    G.add_node(sink)

    for t in range(total_duration + 1):
        G.add_node(f"time_{t}")
    for t in range(total_duration):
        G.add_edge(f"time_{t}", f"time_{t+1}", capacity=1)

    current_time = 0
    for act in valid_activities:
        duration = durations[act - 1]
        start, end = current_time, current_time + duration
        act_node = f"act_{act}"
        G.add_node(act_node)
        G.add_edge(source, act_node, capacity=1)
        G.add_edge(act_node, f"time_{start}", capacity=1)
        G.add_edge(f"time_{end}", sink, capacity=1)
        current_time = end

    return G, source, sink


def compute_max_flow_multiple_methods(ordered_activities, durations):
    """Calcule le flot maximal avec différentes méthodes"""
    results = {}
    max_flow = 0

    # Méthode 1: Graphe de précédence
    try:
        G1, s1, t1 = build_precedence_graph(ordered_activities, durations)
        if G1.number_of_nodes() > 2:  # Plus que source et sink
            flow1, _ = nx.maximum_flow(G1, s1, t1, flow_func=nx.algorithms.flow.edmonds_karp)
            results['precedence'] = flow1
            max_flow = max(max_flow, flow1)
        else:
            results['precedence'] = 0
    except Exception as e:
        results['precedence'] = f"Erreur: {e}"

    # Méthode 2: Contraintes de ressources
    try:
        G2, s2, t2 = build_resource_constraint_graph(ordered_activities, durations)
        if G2.number_of_nodes() > 2:
            flow2, _ = nx.maximum_flow(G2, s2, t2, flow_func=nx.algorithms.flow.edmonds_karp)
            results['resource'] = flow2
            max_flow = max(max_flow, flow2)
        else:
            results['resource'] = 0
    except Exception as e:
        results['resource'] = f"Erreur: {e}"

    # Méthode 3: Calcul direct
    try:
        feasible = len([act for act in ordered_activities if 1 <= act <= len(durations)])
        results['direct'] = feasible
        max_flow = max(max_flow, feasible)
    except Exception as e:
        results['direct'] = f"Erreur: {e}"

    return results, max_flow


def analyze_schedule_quality(ordered_activities, durations):
    """Analyse la qualité de l'ordonnancement"""
    metrics = {}
    valid_activities = [act for act in ordered_activities if 1 <= act <= len(durations)]
    invalid_activities = [act for act in ordered_activities if act < 1 or act > len(durations)]

    total_duration = sum(durations[act - 1] for act in valid_activities) if valid_activities else 0

    metrics['total_duration'] = total_duration
    metrics['valid_activities'] = len(valid_activities)
    metrics['invalid_activities'] = len(invalid_activities)
    metrics['resource_utilization'] = len(valid_activities) / total_duration if total_duration > 0 else 0
    metrics['schedule_efficiency'] = len(valid_activities) / len(ordered_activities) if ordered_activities else 0

    return metrics


def load_ordered_activities_from_json(filepath):
    """Charge les activités ordonnées depuis un fichier JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("ordered_activities", [])
    except Exception as e:
        print(f"Erreur chargement JSON {filepath}: {e}")
        return []


def load_dzn_instance(filepath):
    """Charge une instance DZN avec parsing amélioré"""
    if not os.path.isfile(filepath):
        print(f"Fichier non trouvé: {filepath}")
        return []

    durations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Recherche de patterns plus flexibles pour les durées
        patterns = [
            r'duree\s*=\s*\[([^\]]+)\]',
            r'durations\s*=\s*\[([^\]]+)\]',
            r'duration\s*=\s*\[([^\]]+)\]',
            r'd\s*=\s*\[([^\]]+)\]',
            r'duree\s*=\s*\{([^\}]+)\}',
            r'durations\s*=\s*\{([^\}]+)\}',
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                duration_str = match.group(1)
                # Nettoie et parse les durées
                duration_str = re.sub(r'[,;\s]+', ' ', duration_str.strip())
                try:
                    durations = [int(x) for x in duration_str.split() if x.strip()]
                    if durations:
                        print(f"✓ Durées trouvées: {len(durations)} éléments")
                        return durations
                except ValueError as ve:
                    print(f"Erreur conversion durées: {ve}")
                    continue

        # Si aucun pattern ne fonctionne, essaie une recherche plus générale
        numbers = re.findall(r'\b\d+\b', content)
        if len(numbers) > 5:  # Si on trouve plusieurs nombres, on suppose que ce sont les durées
            durations = [int(x) for x in numbers[:20]]  # Limite à 20 pour éviter les erreurs
            print(f"⚠️ Durées inférées depuis les nombres: {len(durations)} éléments")
            return durations

    except Exception as e:
        print(f"Erreur lecture DZN {filepath}: {e}")

    print(f"❌ Aucune durée trouvée dans {filepath}")
    return []


def export_results_to_csv(all_results, output_path):
    """Exporte les résultats principaux en CSV"""
    headers = ["Instance", "Meilleur_Algorithme", "Flot_Maximal", "Efficacite"] + ALGOS

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for inst in all_results:
            row = [
                inst["instance"], 
                inst["best_algorithm"], 
                inst["best_max_flow"],
                round(inst.get("best_efficiency", 0), 4)
            ]

            for algo in ALGOS:
                val = inst["algorithms_results"].get(algo, {}).get("max_flow", "N/A")
                row.append(val)
            writer.writerow(row)

    print(f"📊 Résultats exportés → {output_path}")


def export_detailed_csv(all_results, output_path):
    """Exporte les résultats détaillés en CSV"""
    headers = [
        "Instance", "Algorithme", "Max_Flow", "Duree_Totale", 
        "Activites_Valides", "Activites_Invalides", "Utilisation_Ressources",
        "Efficacite_Ordonnancement"
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for inst in all_results:
            for algo, data in inst["algorithms_results"].items():
                row = [
                    inst["instance"],
                    algo,
                    data["max_flow"],
                    data["metrics"]["total_duration"],
                    data["metrics"]["valid_activities"],
                    data["metrics"]["invalid_activities"],
                    round(data["metrics"]["resource_utilization"], 4),
                    round(data["metrics"]["schedule_efficiency"], 4)
                ]
                writer.writerow(row)

    print(f"📋 Détails exportés → {output_path}")


def get_instances_from_dzn():
    """Récupère les instances disponibles depuis les fichiers DZN"""
    if not os.path.isdir(INSTANCES_DIR):
        print(f"Répertoire instances non trouvé: {INSTANCES_DIR}")
        return []

    instances = [f[:-4] for f in os.listdir(INSTANCES_DIR) if f.endswith(".dzn")]
    print(f"📁 {len(instances)} instances DZN trouvées")
    return instances


def get_available_results():
    """Récupère les résultats disponibles pour chaque algorithme"""
    results_available = set()
    algos_found = []

    for algo in ALGOS:
        path = os.path.join(RESULTATS_DIR, algo)
        if os.path.isdir(path):
            algo_results = [f[:-5] for f in os.listdir(path) if f.endswith(".json")]
            results_available.update(algo_results)
            algos_found.append(f"{algo}: {len(algo_results)}")
    
    print(f"📊 Résultats trouvés pour: {', '.join(algos_found)}")
    return results_available


def main():
    """Fonction principale"""
    print("🚀 Démarrage de l'analyse des algorithmes d'ordonnancement")

    # Création du répertoire de sortie
    os.makedirs(FORD_FULKERSON_DIR, exist_ok=True)

    # Récupération des instances et résultats
    dzn_instances = get_instances_from_dzn()
    results_available = get_available_results()

    if not dzn_instances:
        print("❌ Aucune instance DZN trouvée")
        return

    if not results_available:
        print("❌ Aucun résultat d'algorithme trouvé")
        return

    # Instances communes
    common = set(dzn_instances) & results_available
    print(f"🔍 {len(common)} instances communes à traiter")

    if not common:
        print("❌ Aucune instance commune entre DZN et résultats")
        return

    all_results = []
    processed = 0
    errors = 0

    for inst in sorted(common):
        print(f"\n🔍 Instance: {inst}")

        # Chargement des durées
        dzn_path = os.path.join(INSTANCES_DIR, f"{inst}.dzn")
        durations = load_dzn_instance(dzn_path)

        if not durations:
            print("⚠️ Durées non chargées.")
            errors += 1
            continue

        # Analyse des algorithmes
        algorithm_results = {}
        for algo in ALGOS:
            filepath = os.path.join(RESULTATS_DIR, algo, f"{inst}.json")
            if not os.path.isfile(filepath):
                continue
            ordered = load_ordered_activities_from_json(filepath)
            if not ordered:
                continue

            # Calcul du flot maximal
            flow_methods, max_flow = compute_max_flow_multiple_methods(ordered, durations)
            metrics = analyze_schedule_quality(ordered, durations)

            algorithm_results[algo] = {
                "max_flow": max_flow,
                "max_flows_details": flow_methods,
                "metrics": metrics
            }

        if not algorithm_results:
            print("⚠️ Aucun résultat d'algorithme valide")
            errors += 1
            continue

        # Sélection du meilleur algorithme
        best_algo, best_data = max(algorithm_results.items(), key=lambda x: x[1]['max_flow'])

        # Construction du résumé
        summary = {
            "instance": inst,
            "best_algorithm": best_algo,
            "best_max_flow": best_data["max_flow"],
            "best_efficiency": best_data["metrics"]["schedule_efficiency"],
            "algorithms_results": algorithm_results,
            "durations_count": len(durations)
        }

        # Sauvegarde JSON
        json_out = os.path.join(FORD_FULKERSON_DIR, f"{inst}.json")
        with open(json_out, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        all_results.append(summary)
        processed += 1

        print(f"✅ Meilleur: {best_algo} (flot: {best_data['max_flow']})")

    # Exportation finale
    print(f"\n📈 Traitement terminé: {processed} instances traitées, {errors} erreurs")

    if all_results:
        export_results_to_csv(all_results, os.path.join(FORD_FULKERSON_DIR, "comparaison_algorithmes.csv"))
        export_detailed_csv(all_results, os.path.join(FORD_FULKERSON_DIR, "resultats_detailles.csv"))

        # Statistiques finales
        best_algos = [r["best_algorithm"] for r in all_results]
        algo_counts = {algo: best_algos.count(algo) for algo in set(best_algos)}
        print(f"🏆 Meilleurs algorithmes: {algo_counts}")
    else:
        print("⚠️ Aucune donnée exportée.")


if __name__ == "__main__":
    main()
