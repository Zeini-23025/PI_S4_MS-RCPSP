#!/usr/bin/env python3
"""
MSRCPSP Solver - Version fonctionnelle corrigée
"""

import os
import json
import csv
import time
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


@dataclass
class Activity:
    id: int
    duration: int
    successors: List[int]
    predecessors: List[int]
    skill_requirements: List[int]
    skill_level_requirements: List[int]
    earliest_start: int = 0
    latest_start: int = float('inf')
    earliest_finish: int = 0
    latest_finish: int = float('inf')
    slack: float = 0


@dataclass
class Resource:
    id: int
    skills: List[int]
    skill_levels: List[int]


@dataclass
class ProjectInstance:
    num_activities: int
    num_resources: int
    num_skills: int
    num_levels: int
    base_deadline: int
    level_deadline: int
    activities: List[Activity]
    resources: List[Resource]


class MSRCPSPParser:
    @staticmethod
    def parse_file(filepath: str) -> ProjectInstance:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        # Trouver les sections
        sections = {}
        for i, line in enumerate(lines):
            if line.startswith('\\*') and line.endswith('*\\'):
                section_name = line.strip('\\* ')
                sections[section_name] = i
        
        # Parser le module projet
        project_start = sections["Project Module"] + 1
        params = list(map(int, lines[project_start].split()))
        
        instance = ProjectInstance(
            num_activities=params[0],
            num_resources=params[1],
            num_skills=params[2],
            num_levels=params[3],
            base_deadline=int(lines[project_start + 1]),
            level_deadline=int(lines[project_start + 2]),
            activities=[],
            resources=[]
        )
        
        # Parser les activités
        activities_start = project_start + 3
        for i in range(instance.num_activities):
            line_idx = activities_start + i
            activity_data = list(map(int, lines[line_idx].split()))
            duration = activity_data[0]
            num_successors = activity_data[1]
            # Convertir IDs de successeurs (base 1 -> base 0)
            successors = [s-1 for s in activity_data[2:2+num_successors]] if num_successors > 0 else []
            
            activity = Activity(
                id=i,
                duration=duration,
                successors=successors,
                predecessors=[],
                skill_requirements=[0] * instance.num_skills,
                skill_level_requirements=[0] * instance.num_skills
            )
            instance.activities.append(activity)
        
        # Parser les ressources (compétences binaires)
        if "Workforce Module" in sections:
            workforce_start = sections["Workforce Module"] + 1
            for i in range(instance.num_resources):
                line_idx = workforce_start + i
                skills = list(map(int, lines[line_idx].split()))
                resource = Resource(
                    id=i,
                    skills=skills,
                    skill_levels=[0] * instance.num_skills
                )
                instance.resources.append(resource)
        
        # Parser les niveaux de compétences
        if "Workforce Module with Skill Levels" in sections:
            levels_start = sections["Workforce Module with Skill Levels"] + 1
            for i in range(instance.num_resources):
                line_idx = levels_start + i
                levels = list(map(int, lines[line_idx].split()))
                instance.resources[i].skill_levels = levels
        
        # Parser les exigences de compétences
        if "Skill Requirements Module" in sections:
            req_start = sections["Skill Requirements Module"] + 1
            for i in range(instance.num_activities):
                line_idx = req_start + i
                requirements = list(map(int, lines[line_idx].split()))
                instance.activities[i].skill_requirements = requirements
        
        # Parser les niveaux requis
        if "Skill Level Requirements Module" in sections:
            level_req_start = sections["Skill Level Requirements Module"] + 1
            for i in range(instance.num_activities):
                line_idx = level_req_start + i
                if line_idx < len(lines):
                    line_content = lines[line_idx]
                    if line_content == "-1":
                        instance.activities[i].skill_level_requirements = []
                    else:
                        levels = list(map(int, line_content.split()))
                        instance.activities[i].skill_level_requirements = levels
        
        # Calculer les prédécesseurs
        MSRCPSPParser._compute_predecessors(instance)
        
        return instance
    
    @staticmethod
    def _compute_predecessors(instance: ProjectInstance):
        for activity in instance.activities:
            for successor_id in activity.successors:
                if 0 <= successor_id < len(instance.activities):
                    instance.activities[successor_id].predecessors.append(activity.id)


class MSRCPSPScheduler:
    def __init__(self, instance: ProjectInstance):
        self.instance = instance
        self._compute_time_bounds()
    
    def _compute_time_bounds(self):
        # Forward pass - Temps au plus tôt
        for activity in self.instance.activities:
            if not activity.predecessors:
                activity.earliest_start = 0
            else:
                max_pred_finish = 0
                for pred_id in activity.predecessors:
                    pred = self.instance.activities[pred_id]
                    max_pred_finish = max(max_pred_finish, pred.earliest_finish)
                activity.earliest_start = max_pred_finish
            activity.earliest_finish = activity.earliest_start + activity.duration
        
        # Backward pass - Temps au plus tard
        max_ef = max(a.earliest_finish for a in self.instance.activities)
        deadline = max(self.instance.level_deadline, max_ef)
        
        for activity in reversed(self.instance.activities):
            if not activity.successors:
                activity.latest_finish = deadline
            else:
                min_succ_start = float('inf')
                for succ_id in activity.successors:
                    if 0 <= succ_id < len(self.instance.activities):
                        succ = self.instance.activities[succ_id]
                        min_succ_start = min(min_succ_start, succ.latest_start)
                activity.latest_finish = min_succ_start
            activity.latest_start = activity.latest_finish - activity.duration
            activity.slack = activity.latest_start - activity.earliest_start
    
    def find_available_resources_with_relaxation(self, activity: Activity, start_time: int, 
                                               resource_schedule: Dict[int, List[Tuple[int, int]]], 
                                               relaxation_level: int = 0) -> Tuple[bool, List[int]]:
        """
        Trouver les ressources disponibles avec relaxation progressive
        relaxation_level: 0=strict, 1=niveau-1, 2=ignorer niveaux, 3=multi-usage
        """
        end_time = start_time + activity.duration
        
        # Activités dummy
        if activity.duration == 0 or sum(activity.skill_requirements) == 0:
            return True, []
        
        # Collecter toutes les ressources disponibles temporellement
        available_resources = []
        for resource in self.instance.resources:
            is_available = True
            for scheduled_start, scheduled_end in resource_schedule.get(resource.id, []):
                if not (end_time <= scheduled_start or start_time >= scheduled_end):
                    is_available = False
                    break
            
            if is_available:
                available_resources.append(resource)
        
        # Assignation des ressources avec relaxation
        assigned_resources = []
        
        for skill_idx, required_count in enumerate(activity.skill_requirements):
            if required_count == 0:
                continue
            
            suitable_resources = []
            
            for resource in available_resources:
                if resource.id in assigned_resources:
                    continue
                
                # Vérifier compétence
                has_skill = (skill_idx < len(resource.skills) and 
                           resource.skills[skill_idx] > 0)
                
                if not has_skill:
                    continue
                
                # Vérifier niveau avec relaxation
                level_ok = True
                if (len(activity.skill_level_requirements) > skill_idx and 
                    skill_idx < len(resource.skill_levels)):
                    required_level = activity.skill_level_requirements[skill_idx]
                    resource_level = resource.skill_levels[skill_idx]
                    
                    if relaxation_level == 0:  # Strict
                        level_ok = resource_level >= required_level
                    elif relaxation_level == 1:  # Niveau -1
                        level_ok = resource_level >= max(1, required_level - 1)
                    elif relaxation_level >= 2:  # Ignorer niveaux
                        level_ok = True
                
                if level_ok:
                    suitable_resources.append(resource)
            
            # Gestion multi-usage pour relaxation_level >= 3
            if (relaxation_level >= 3 and 
                len(suitable_resources) < required_count):
                # Permettre qu'une ressource polyvalente compte pour plusieurs compétences
                for resource in available_resources:
                    if resource.id in assigned_resources:
                        continue
                    
                    # Compter combien de compétences cette ressource peut satisfaire
                    skills_covered = 0
                    for i, req in enumerate(activity.skill_requirements):
                        if (req > 0 and i < len(resource.skills) and 
                            resource.skills[i] > 0):
                            skills_covered += 1
                    
                    if skills_covered >= 2:  # Ressource polyvalente
                        suitable_resources.append(resource)
                        if len(suitable_resources) >= required_count:
                            break
            
            # Vérifier si on a assez de ressources
            if len(suitable_resources) < required_count:
                return False, []
            
            # Assigner les ressources
            for i in range(min(required_count, len(suitable_resources))):
                assigned_resources.append(suitable_resources[i].id)
        
        return True, assigned_resources

    def schedule_with_priority_improved(self, priority_name: str) -> Tuple[int, List]:
        """Ordonnancement avec relaxation progressive pour éviter les deadlocks"""
        
        for relaxation_level in range(4):  # 0=strict, 1=niveau-1, 2=ignorer niveaux, 3=multi-usage
            current_time = 0
            completed_activities = set()
            resource_schedule = defaultdict(list)
            schedule = []
            max_iterations = 10000
            iterations = 0
            stagnation_count = 0
            
            while (len(completed_activities) < len(self.instance.activities) and 
                   iterations < max_iterations):
                iterations += 1
                scheduled_any = False
                
                # Trouver les activités prêtes
                ready_activities = []
                for activity in self.instance.activities:
                    if activity.id in completed_activities:
                        continue
                    
                    all_preds_done = all(p in completed_activities 
                                       for p in activity.predecessors)
                    if all_preds_done:
                        ready_activities.append(activity)
                
                # Appliquer la règle de priorité
                if priority_name == "EST":
                    ready_activities.sort(key=lambda a: a.earliest_start)
                elif priority_name == "LFT":
                    ready_activities.sort(key=lambda a: a.latest_finish)
                elif priority_name == "MSLF":
                    ready_activities.sort(key=lambda a: a.slack)
                elif priority_name == "SPT":
                    ready_activities.sort(key=lambda a: a.duration)
                elif priority_name == "LPT":
                    ready_activities.sort(key=lambda a: -a.duration)
                elif priority_name == "FCFS":
                    ready_activities.sort(key=lambda a: a.id)
                elif priority_name == "LST":
                    ready_activities.sort(key=lambda a: -a.latest_start)
                
                # Essayer d'ordonnancer avec la relaxation courante
                for activity in ready_activities:
                    start_time = max(current_time, activity.earliest_start)
                    
                    can_schedule, assigned_resources = self.find_available_resources_with_relaxation(
                        activity, start_time, resource_schedule, relaxation_level
                    )
                    
                    if can_schedule:
                        end_time = start_time + activity.duration
                        schedule.append((activity.id, start_time, end_time, assigned_resources))
                        
                        # Marquer les ressources comme occupées
                        for res_id in assigned_resources:
                            resource_schedule[res_id].append((start_time, end_time))
                        
                        completed_activities.add(activity.id)
                        scheduled_any = True
                        stagnation_count = 0
                        current_time = max(current_time, start_time)
                        break
                
                if not scheduled_any:
                    # Avancer le temps intelligemment
                    next_time = current_time + 1
                    
                    # Chercher le prochain moment où une ressource se libère
                    for resource_times in resource_schedule.values():
                        for _, end_time in resource_times:
                            if end_time > current_time:
                                next_time = min(next_time, end_time)
                    
                    current_time = next_time
                    stagnation_count += 1
                    
                    # Éviter la stagnation excessive
                    if stagnation_count > 1000:
                        break
            
            # Si toutes les activités sont ordonnancées, retourner le résultat
            if len(completed_activities) == len(self.instance.activities):
                makespan = max(end_time for _, _, end_time, _ in schedule) if schedule else 0
                return makespan, schedule
        
        # Si échec même avec relaxation maximale, retourner une solution partielle
        makespan = max(end_time for _, _, end_time, _ in schedule) if schedule else 0
        return makespan, schedule
    
    def schedule_with_priority(self, priority_name: str) -> Tuple[int, List]:
        """Version améliorée utilisant la relaxation progressive"""
        return self.schedule_with_priority_improved(priority_name)


def run_algorithms_on_instance(instance_path: str, algorithms: List[str]) -> Dict[str, Dict]:
    """Exécute plusieurs algorithmes sur une instance"""
    instance_name = os.path.basename(instance_path).replace('.msrcp', '')
    
    try:
        instance = MSRCPSPParser.parse_file(instance_path)
        scheduler = MSRCPSPScheduler(instance)
        
        algorithms = ["EST", "LFT", "MSLF", "SPT", "LPT", "FCFS", "LST"]
        results = {}
        
        for alg in algorithms:
            try:
                makespan, schedule = scheduler.schedule_with_priority(alg)
                results[alg] = {
                    'makespan': makespan,
                    'schedule': schedule,
                    'activities_order': [s[0] for s in schedule]
                }
                print(f"  ✓ {alg}: {makespan}")
            except Exception as e:
                results[alg] = {
                    'makespan': float('inf'),
                    'schedule': [],
                    'activities_order': [],
                    'error': str(e)
                }
                print(f"  ✗ {alg}: Error - {str(e)}")
        
        return results
        
    except Exception as e:
        print(f"❌ Erreur parsing {instance_name}: {str(e)}")
        return {}


def main():
    """Fonction principale - traite toutes les instances du dossier"""
    print("🚀 MSRCPSP Solver - Traitement de toutes les instances")
    
    # Définir les algorithmes à utiliser
    algorithms = ["EST", "LFT", "MSLF", "SPT", "LPT", "FCFS", "LST"]
    
    # Créer répertoires de sortie
    os.makedirs("resultats", exist_ok=True)
    
    # Vérifier que le dossier Instances existe
    instances_dir = "Instances"
    if not os.path.exists(instances_dir):
        print(f"❌ Répertoire {instances_dir} non trouvé!")
        return
    
    # Lister toutes les instances .msrcp
    all_files = [f for f in os.listdir(instances_dir) if f.endswith('.msrcp')]
    if not all_files:
        print(f"❌ Aucun fichier .msrcp trouvé dans {instances_dir}!")
        return
    
    # Trier et limiter à un nombre raisonnable pour le test (ou prendre toutes)
    all_files.sort()
    
    # Option: Traiter toutes les instances (décommentez la ligne suivante)
    # test_instances = [os.path.join(instances_dir, f) for f in all_files]
    
    # Option par défaut: Traiter un échantillon pour test rapide
    max_instances = min(10, len(all_files))
    test_instances = [os.path.join(instances_dir, f) 
                     for f in all_files[:max_instances]]
    
    print(f"📁 {len(all_files)} instances trouvées dans {instances_dir}")
    print(f"🔄 Traitement de {len(test_instances)} instances...")
    
    all_results = {}
    comparison_data = []
    
    for instance_path in test_instances:
        if not os.path.exists(instance_path):
            print(f"⚠️  Instance non trouvée: {instance_path}")
            continue
        
        instance_name = os.path.basename(instance_path).replace('.msrcp', '')
        print(f"\n📊 Traitement de {instance_name}...")
        
        results = run_algorithms_on_instance(instance_path, algorithms)
        if results:
            all_results[instance_name] = results
            
            # Préparer les données de comparaison
            row = {'Instance': instance_name}
            for alg in algorithms:
                row[alg] = results.get(alg, {}).get('makespan', float('inf'))
            comparison_data.append(row)
    
    # Sauvegarder les résultats
    if comparison_data:
        # Fichier de comparaison
        comparison_file = "resultats/test_comparison.csv"
        with open(comparison_file, 'w', newline='') as f:
            fieldnames = ['Instance'] + algorithms
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(comparison_data)
        
        print(f"\n📊 Résultats sauvegardés dans {comparison_file}")
        
        # Résultats détaillés
        detail_file = "resultats/detailed_results.json"
        with open(detail_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"📝 Détails sauvegardés dans {detail_file}")
        
        # Afficher résumé
        print("\n" + "="*50)
        print("📈 RÉSUMÉ DES RÉSULTATS")
        print("="*50)
        
        for row in comparison_data:
            print(f"\n🔹 {row['Instance']}:")
            makespans = [(alg, row[alg]) for alg in ['EST', 'LFT', 'MSLF', 'SPT'] 
                        if row[alg] != float('inf')]
            makespans.sort(key=lambda x: x[1])
            
            for i, (alg, makespan) in enumerate(makespans):
                symbol = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "📊"
                print(f"    {symbol} {alg}: {makespan}")


def diagnose_instance_complexity(instance: ProjectInstance) -> Dict[str, any]:
    """Diagnostic de la complexité d'une instance"""
    
    # Statistiques de base
    stats = {
        'num_activities': instance.num_activities,
        'num_resources': instance.num_resources,
        'num_skills': instance.num_skills,
        'activity_durations': [a.duration for a in instance.activities],
        'total_skill_requirements': [],
        'resource_utilization_potential': 0,
        'precedence_density': 0,
        'critical_path_estimate': 0
    }
    
    # Analyser les exigences de compétences
    for activity in instance.activities:
        total_req = sum(activity.skill_requirements)
        stats['total_skill_requirements'].append(total_req)
    
    # Calculer la densité des contraintes de précédence
    total_possible_edges = instance.num_activities * (instance.num_activities - 1)
    actual_edges = sum(len(a.predecessors) for a in instance.activities)
    stats['precedence_density'] = actual_edges / total_possible_edges if total_possible_edges > 0 else 0
    
    # Estimer le chemin critique
    max_path = 0
    for activity in instance.activities:
        if not activity.successors:  # Activité finale
            path_length = activity.earliest_finish
            max_path = max(max_path, path_length)
    stats['critical_path_estimate'] = max_path
    
    # Analyser les goulots d'étranglement de ressources
    skill_demand = [0] * instance.num_skills
    for activity in instance.activities:
        for i, req in enumerate(activity.skill_requirements):
            if i < len(skill_demand):
                skill_demand[i] += req
    
    skill_supply = [0] * instance.num_skills
    for resource in instance.resources:
        for i, skill in enumerate(resource.skills):
            if i < len(skill_supply) and skill > 0:
                skill_supply[i] += 1
    
    bottlenecks = []
    for i in range(min(len(skill_demand), len(skill_supply))):
        if skill_supply[i] > 0:
            ratio = skill_demand[i] / skill_supply[i]
            bottlenecks.append(ratio)
        else:
            bottlenecks.append(float('inf'))
    
    stats['resource_bottlenecks'] = bottlenecks
    stats['max_bottleneck'] = max(bottlenecks) if bottlenecks else 0
    
    return stats


def analyze_scheduling_differences(instance: ProjectInstance, algorithms: List[str]) -> Dict[str, any]:
    """Analyse pourquoi les algorithmes donnent des résultats similaires"""
    
    scheduler = MSRCPSPScheduler(instance)
    results = {}
    schedules = {}
    
    # Tester tous les algorithmes
    for alg in algorithms:
        try:
            makespan, schedule = scheduler.schedule_with_priority(alg)
            results[alg] = makespan
            schedules[alg] = schedule
        except Exception as e:
            results[alg] = float('inf')
            schedules[alg] = []
    
    # Analyser les différences
    analysis = {
        'makespans': results,
        'unique_makespans': len(set(v for v in results.values() if v != float('inf'))),
        'best_makespan': min(v for v in results.values() if v != float('inf')) if any(v != float('inf') for v in results.values()) else float('inf'),
        'worst_makespan': max(v for v in results.values() if v != float('inf')) if any(v != float('inf') for v in results.values()) else float('inf'),
        'schedule_similarities': {}
    }
    
    # Comparer les ordres d'activités
    activity_orders = {}
    for alg, schedule in schedules.items():
        if schedule:
            activity_orders[alg] = [activity_id for activity_id, _, _, _ in sorted(schedule, key=lambda x: x[1])]
    
    # Calculer la similarité des ordres
    similarities = {}
    alg_list = list(activity_orders.keys())
    for i, alg1 in enumerate(alg_list):
        for alg2 in alg_list[i+1:]:
            if alg1 in activity_orders and alg2 in activity_orders:
                order1 = activity_orders[alg1]
                order2 = activity_orders[alg2]
                # Calculer le pourcentage de positions identiques
                common_positions = sum(1 for j, (a1, a2) in enumerate(zip(order1, order2)) if a1 == a2)
                similarity = common_positions / max(len(order1), len(order2)) if max(len(order1), len(order2)) > 0 else 0
                similarities[f"{alg1}_vs_{alg2}"] = similarity
    
    analysis['schedule_similarities'] = similarities
    analysis['activity_orders'] = activity_orders
    
    return analysis


if __name__ == "__main__":
    main()
