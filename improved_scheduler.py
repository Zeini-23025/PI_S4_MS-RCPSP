#!/usr/bin/env python3
"""
Version améliorée du scheduler MSRCPSP avec backtracking et relaxation
"""

import os
import copy
from msrcpsp_final import MSRCPSPParser, ProjectInstance, Activity, Resource
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class ImprovedMSRCPSPScheduler:
    def __init__(self, instance: ProjectInstance):
        self.instance = instance
        self._compute_time_bounds()
    
    def _compute_time_bounds(self):
        """Calcul des bornes temporelles avec logique robuste"""
        # Forward pass - Temps au plus tôt
        for activity in self.instance.activities:
            if not activity.predecessors:
                activity.earliest_start = 0
            else:
                max_pred_finish = 0
                for pred_id in activity.predecessors:
                    if pred_id < len(self.instance.activities):
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

    def find_available_resources(self, activity: Activity, start_time: int, 
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

    def schedule_with_progressive_relaxation(self, priority_name: str) -> Tuple[int, List]:
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
                    
                    can_schedule, assigned_resources = self.find_available_resources(
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


def test_improved_scheduler():
    """Test du scheduler amélioré"""
    print("🧪 TEST DU SCHEDULER AMÉLIORÉ")
    print("=" * 50)
    
    instances_dir = "Instances"
    test_files = [
        "MSLIB_Set1_1000.msrcp",
        "MSLIB_Set1_1001.msrcp", 
        "MSLIB_Set1_1003.msrcp",
        "MSLIB_Set1_101.msrcp",
        "MSLIB_Set1_1.msrcp"
    ]
    
    algorithms = ["EST", "LFT", "MSLF", "SPT", "LPT", "FCFS", "LST"]
    
    for filename in test_files:
        filepath = os.path.join(instances_dir, filename)
        if not os.path.exists(filepath):
            continue
        
        print(f"\n📊 {filename}")
        print("-" * 40)
        
        try:
            instance = MSRCPSPParser.parse_file(filepath)
            scheduler = ImprovedMSRCPSPScheduler(instance)
            
            results = {}
            for alg in algorithms:
                makespan, schedule = scheduler.schedule_with_progressive_relaxation(alg)
                activities_scheduled = len(schedule)
                results[alg] = makespan
                
                status = "✅" if activities_scheduled == instance.num_activities else "⚠️"
                print(f"  {alg:4s}: {status} makespan={makespan:3d}, activités={activities_scheduled:2d}/{instance.num_activities}")
            
            # Analyser la diversité
            unique_results = len(set(results.values()))
            best = min(results.values())
            worst = max(results.values())
            
            print(f"  📈 Diversité: {unique_results}/7 résultats uniques")
            print(f"  📈 Plage: {best} - {worst}")
            
        except Exception as e:
            print(f"  ❌ Erreur: {str(e)}")


if __name__ == "__main__":
    test_improved_scheduler()
