import os
import json
import csv
import glob
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import pandas as pd


class MSRCPSPScheduler:
    """
    Classe pour calculer le makespan (durée totale) d'un ordonnancement
    en tenant compte des contraintes de ressources et compétences
    """
    
    def __init__(self, instance_data: Dict[str, Any]):
        self.data = instance_data
        self.n_activities = self.data.get('nActs', 0)
        self.n_resources = self.data.get('nRes', 0)
        self.n_skills = self.data.get('nSkills', 0)
        
        self.durations = self.data.get('dur', [1] * self.n_activities)
        self.precedence_graph = self.data.get('precedence_graph', {})
        
        # Données de compétences
        self.skill_requirements = self.data.get('sreq', [])
        self.resource_mastery = self.data.get('mastery', [])
        
        # Capacités des ressources
        self.resource_capacity = self.data.get('capacity', [1] * self.n_resources)
        self.resource_availability = [0] * max(1, self.n_resources)
        
    def calculate_makespan(self, activity_order: List[int]) -> Tuple[int, Dict[int, Tuple[int, int]]]:
        """
        Calcule le makespan pour un ordre d'activités donné
        Retourne (makespan, schedule) où schedule[activity] = (start_time, end_time)
        """
        schedule = {}  # activity -> (start_time, end_time)
        resource_availability = [0] * max(1, self.n_resources)  # Temps de libération de chaque ressource
        
        for activity in activity_order:
            activity_idx = activity - 1
            duration = self.durations[activity_idx]
            
            # Calculer le temps de début le plus tôt selon les précédences
            earliest_start = 0
            predecessors = self.precedence_graph.get(activity, {}).get('predecessors', [])
            
            for pred in predecessors:
                if pred in schedule:
                    pred_end_time = schedule[pred][1]
                    earliest_start = max(earliest_start, pred_end_time)
            
            # Trouver les ressources nécessaires et disponibles
            required_resources = self._find_required_resources(activity)
            
            if not required_resources:
                # Activité sans contrainte de ressource
                start_time = earliest_start
                end_time = start_time + duration
            else:
                # Trouver le moment où toutes les ressources nécessaires sont disponibles
                start_time = self._find_earliest_resource_availability(
                    required_resources, earliest_start, duration, resource_availability
                )
                end_time = start_time + duration
                
                # Mettre à jour la disponibilité des ressources
                for resource_idx in required_resources:
                    if resource_idx < len(resource_availability):
                        resource_availability[resource_idx] = end_time
            
            schedule[activity] = (start_time, end_time)
        
        # Le makespan est le temps de fin maximum
        makespan = max(end_time for _, end_time in schedule.values()) if schedule else 0
        
        return makespan, schedule
    
    def _find_required_resources(self, activity: int) -> List[int]:
        """
        Trouve les ressources nécessaires pour une activité
        en tenant compte des compétences requises
        """
        activity_idx = activity - 1
        
        # Si pas de données de compétences, supposer qu'une ressource est nécessaire
        if not self.skill_requirements or activity_idx >= len(self.skill_requirements):
            return [0] if self.n_resources > 0 else []
        
        required_skills = self.skill_requirements[activity_idx]
        
        # Trouver une ressource capable d'exécuter la tâche
        capable_resources = []
        
        for resource_idx, masteries in enumerate(self.resource_mastery):
            if resource_idx >= self.n_resources:
                break
                
            # Vérifier si cette ressource maîtrise toutes les compétences requises
            can_do_task = all(
                not required_skills[skill_idx] or 
                (skill_idx < len(masteries) and masteries[skill_idx])
                for skill_idx in range(len(required_skills))
            )
            
            if can_do_task:
                capable_resources.append(resource_idx)
        
        # Retourner la première ressource capable (stratégie simple)
        return capable_resources[:1] if capable_resources else [0]
    
    def _find_earliest_resource_availability(
            self, required_resources: List[int],
            earliest_start: int, duration: int,
            resource_availability: List[int]) -> int:
        """
        Trouve le moment le plus tôt où toutes les ressources requises
        sont disponibles
        """
        if not required_resources:
            return earliest_start
        
        # Pour simplifier, on prend le maximum des temps de libération
        max_resource_availability = max(
            (resource_availability[res_idx]
             if res_idx < len(resource_availability) else 0)
            for res_idx in required_resources
        )
        
        return max(earliest_start, max_resource_availability)


class MakespanCalculator:
    """
    Classe principale pour calculer et comparer les makespans
    """
    
    def __init__(self, results_dir: str = "./resultats", instances_dir: str = "./instances"):
        self.results_dir = results_dir
        self.instances_dir = instances_dir
        self.algorithms = ['HRPW*', 'LST', 'LFT', 'MTS', 'TIMROS', 'HRU1', 'TIMRES', 'HRU2', 'STFD', 'EFT']
    
    def load_instance_data(self, instance_name: str) -> Dict[str, Any]:
        """Charge les données d'une instance depuis le fichier .dzn"""
        from paste import parse_dzn_file, compute_temporal_metrics
        
        dzn_file = os.path.join(self.instances_dir, f"{instance_name}.dzn")
        if not os.path.exists(dzn_file):
            raise FileNotFoundError(f"Instance file not found: {dzn_file}")
        
        instance_data = parse_dzn_file(dzn_file)
        instance_data = compute_temporal_metrics(instance_data)
        
        return instance_data
    
    def load_algorithm_result(self, algorithm: str, instance_name: str) -> List[int]:
        """Charge le résultat d'un algorithme pour une instance"""
        result_file = os.path.join(self.results_dir, algorithm, f"{instance_name}.json")
        
        if not os.path.exists(result_file):
            raise FileNotFoundError(f"Result file not found: {result_file}")
        
        with open(result_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('ordered_activities', [])
    
    def calculate_all_makespans(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Calcule les makespans pour toutes les instances et tous les algorithmes
        Retourne: {instance_name: {algorithm: {makespan, schedule, execution_time}}}
        """
        results = defaultdict(lambda: defaultdict(dict))
        
        # Trouver toutes les instances
        instance_files = []
        for algorithm in self.algorithms:
            algo_dir = os.path.join(self.results_dir, algorithm)
            if os.path.exists(algo_dir):
                json_files = glob.glob(os.path.join(algo_dir, "*.json"))
                for json_file in json_files:
                    instance_name = os.path.splitext(os.path.basename(json_file))[0]
                    if instance_name not in instance_files:
                        instance_files.append(instance_name)
        
        print(f"Calcul des makespans pour {len(instance_files)} instance(s)...")
        
        for instance_name in instance_files:
            print(f"\nTraitement de l'instance: {instance_name}")
            
            try:
                # Charger les données de l'instance
                instance_data = self.load_instance_data(instance_name)
                scheduler = MSRCPSPScheduler(instance_data)
                
                # Calculer le makespan pour chaque algorithme
                for algorithm in self.algorithms:
                    try:
                        # Charger l'ordre des activités
                        activity_order = self.load_algorithm_result(algorithm, instance_name)
                        
                        # Calculer le makespan
                        import time
                        start_time = time.time()
                        makespan, schedule = scheduler.calculate_makespan(activity_order)
                        execution_time = time.time() - start_time
                        
                        results[instance_name][algorithm] = {
                            'makespan': makespan,
                            'schedule': schedule,
                            'execution_time': execution_time,
                            'activity_order': activity_order
                        }
                        
                        print(f"  {algorithm}: makespan = {makespan}")
                        
                    except FileNotFoundError:
                        print(f"  {algorithm}: fichier résultat manquant")
                        results[instance_name][algorithm] = {
                            'makespan': float('inf'),
                            'schedule': {},
                            'execution_time': 0,
                            'activity_order': []
                        }
                    except Exception as e:
                        print(f"  {algorithm}: erreur - {str(e)}")
                        results[instance_name][algorithm] = {
                            'makespan': float('inf'),
                            'schedule': {},
                            'execution_time': 0,
                            'activity_order': []
                        }
            
            except Exception as e:
                print(f"Erreur lors du traitement de {instance_name}: {str(e)}")
        
        return dict(results)
    
    def save_detailed_results(self, results: Dict[str, Dict[str, Dict[str, Any]]]):
        """Sauvegarde les résultats détaillés pour chaque instance et algorithme"""
        detailed_dir = os.path.join(self.results_dir, "makespan_details")
        os.makedirs(detailed_dir, exist_ok=True)
        
        for instance_name, instance_results in results.items():
            output_file = os.path.join(detailed_dir, f"{instance_name}_makespans.json")
            
            # Préparer les données pour la sauvegarde (convertir les tuples en listes)
            serializable_results = {}
            for algorithm, result in instance_results.items():
                schedule_serializable = {
                    str(activity): [start, end] 
                    for activity, (start, end) in result['schedule'].items()
                }
                
                serializable_results[algorithm] = {
                    'makespan': result['makespan'],
                    'execution_time': result['execution_time'],
                    'schedule': schedule_serializable,
                    'activity_order': result['activity_order']
                }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'instance': instance_name,
                    'results': serializable_results
                }, f, indent=2, ensure_ascii=False)
        
        print(f"\nRésultats détaillés sauvegardés dans {detailed_dir}")
    
    def create_comparison_csv(self, results: Dict[str, Dict[str, Dict[str, Any]]]):
        """Crée un fichier CSV de comparaison des résultats"""
        csv_file = os.path.join(self.results_dir, "makespan_comparison.csv")
        
        # Préparer les données pour le CSV
        csv_data = []
        
        for instance_name, instance_results in results.items():
            row = {'Instance': instance_name}
            
            # Ajouter les makespans pour chaque algorithme
            for algorithm in self.algorithms:
                makespan = instance_results.get(algorithm, {}).get('makespan', float('inf'))
                row[f'{algorithm}_Makespan'] = makespan if makespan != float('inf') else 'N/A'
                
                exec_time = instance_results.get(algorithm, {}).get('execution_time', 0)
                row[f'{algorithm}_Time'] = f"{exec_time:.4f}"
            
            # Trouver le meilleur algorithme
            valid_makespans = {
                alg: res['makespan'] 
                for alg, res in instance_results.items() 
                if res['makespan'] != float('inf')
            }
            
            if valid_makespans:
                best_algorithm = min(valid_makespans.keys(), key=lambda x: valid_makespans[x])
                best_makespan = valid_makespans[best_algorithm]
                row['Best_Algorithm'] = best_algorithm
                row['Best_Makespan'] = best_makespan
                
                # Calculer les écarts par rapport au meilleur
                for algorithm in self.algorithms:
                    if algorithm in valid_makespans:
                        gap = ((valid_makespans[algorithm] - best_makespan) / best_makespan) * 100
                        row[f'{algorithm}_Gap'] = f"{gap:.2f}%"
                    else:
                        row[f'{algorithm}_Gap'] = 'N/A'
            else:
                row['Best_Algorithm'] = 'N/A'
                row['Best_Makespan'] = 'N/A'
            
            csv_data.append(row)
        
        # Créer le DataFrame et sauvegarder
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        print(f"Fichier de comparaison CSV créé: {csv_file}")
        
        return csv_file
    
    def create_summary_statistics(self, results: Dict[str, Dict[str, Dict[str, Any]]]):
        """Crée des statistiques de résumé"""
        summary_file = os.path.join(self.results_dir, "summary_statistics.csv")
        
        # Calculer les statistiques pour chaque algorithme
        stats_data = []
        
        for algorithm in self.algorithms:
            makespans = []
            execution_times = []
            wins = 0
            
            for instance_name, instance_results in results.items():
                # Correction : ignorer les résultats qui ne sont pas des dicts (ex: listes)
                algo_result = instance_results.get(algorithm, {})
                if not isinstance(algo_result, dict):
                    continue
                makespan = algo_result.get('makespan', float('inf'))
                if makespan != float('inf'):
                    makespans.append(makespan)
                    execution_times.append(algo_result.get('execution_time', 0))
                    
                    # Vérifier si c'est le meilleur pour cette instance
                    all_makespans = [
                        res['makespan'] for res in instance_results.values()
                        if isinstance(res, dict) and res.get('makespan', float('inf')) != float('inf')
                    ]
                    if all_makespans and makespan == min(all_makespans):
                        wins += 1
            
            if makespans:
                stats_data.append({
                    'Algorithm': algorithm,
                    'Avg_Makespan': sum(makespans) / len(makespans),
                    'Min_Makespan': min(makespans),
                    'Max_Makespan': max(makespans),
                    'Std_Makespan': pd.Series(makespans).std(),
                    'Avg_Time': sum(execution_times) / len(execution_times),
                    'Wins': wins,
                    'Success_Rate': (len(makespans) / len(results)) * 100
                })
        
        # Créer le DataFrame et sauvegarder
        df_stats = pd.DataFrame(stats_data)
        if not df_stats.empty and 'Avg_Makespan' in df_stats.columns:
            df_stats = df_stats.sort_values('Avg_Makespan')
        df_stats.to_csv(summary_file, index=False, encoding='utf-8')
        
        print(f"Statistiques de résumé créées: {summary_file}")
        
        return summary_file
    
    def run_complete_analysis(self):
        """Exécute l'analyse complète"""
        print("=" * 60)
        print("ANALYSE COMPLÈTE DES MAKESPANS MS-RCPSP")
        print("=" * 60)
        
        # Calculer tous les makespans
        results = self.calculate_all_makespans()
        
        if not results:
            print("Aucun résultat trouvé!")
            return
        
        # Sauvegarder les résultats détaillés
        self.save_detailed_results(results)
        
        # Créer le fichier de comparaison CSV
        comparison_file = self.create_comparison_csv(results)
        
        # Créer les statistiques de résumé
        summary_file = self.create_summary_statistics(results)
        
        # Afficher un résumé
        print("\n" + "=" * 60)
        print("RÉSUMÉ DE L'ANALYSE")
        print("=" * 60)
        
        total_instances = len(results)
        print(f"Instances traitées: {total_instances}")
        print(f"Algorithmes testés: {len(self.algorithms)}")
        
        # Compter les succès par algorithme
        algorithm_success = defaultdict(int)
        for instance_results in results.values():
            for algorithm, result in instance_results.items():
                if result['makespan'] != float('inf'):
                    algorithm_success[algorithm] += 1
        
        print("\nTaux de succès par algorithme:")
        for algorithm in self.algorithms:
            success_rate = (algorithm_success[algorithm] / total_instances) * 100
            print(f"  {algorithm}: {success_rate:.1f}% ({algorithm_success[algorithm]}/{total_instances})")
        
        print(f"\nFichiers générés:")
        print(f"  - Comparaison détaillée: {comparison_file}")
        print(f"  - Statistiques résumées: {summary_file}")

        # Déterminer et afficher le best algorithme global
        try:
            df_stats = pd.read_csv(summary_file)
            if not df_stats.empty and 'Avg_Makespan' in df_stats.columns:
                best_overall_algo_row = df_stats.loc[df_stats['Avg_Makespan'].idxmin()]
                print("\n" + "=" * 60)
                print("MEILLEUR ALGORITHME GLOBAL (basé sur le Makespan Moyen)")
                print("=" * 60)
                print(f"Algorithme: {best_overall_algo_row['Algorithm']}")
                print(f"Makespan Moyen: {best_overall_algo_row['Avg_Makespan']:.2f}")
                print(f"Nombre de Victoires: {int(best_overall_algo_row['Wins'])}")
                print(f"Taux de Succès: {best_overall_algo_row['Success_Rate']:.2f}%")
            else:
                print("\nImpossible de déterminer le best algorithme global (données statistiques manquantes ou vides).")
        except Exception as e:
            print(f"\nErreur lors de la détermination du best algorithme global: {e}")
        print(f"  - Résultats détaillés: {os.path.join(self.results_dir, 'makespan_details')}")


def main():
    """Fonction principale"""
    calculator = MakespanCalculator()
    calculator.run_complete_analysis()


if __name__ == "__main__":
    main()
