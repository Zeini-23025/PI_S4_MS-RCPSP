import os
import re
import glob
import networkx as nx
import json
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict, deque


class MSRCPSPPriorityAlgorithms:
    """
    Classe pour les algorithmes de priorité dans le MS-RCPSP
    (Multi-Skill Resource-Constrained Project Scheduling Problem)
    """
    
    def __init__(self, instance_data: Dict[str, Any]):
        self.data = instance_data
        self.n_activities = self.data.get('nActs', 0)
        self.n_resources = self.data.get('nRes', 0)
        self.n_skills = self.data.get('nSkills', 0)
        
        # Données de base
        self.activities = list(range(1, self.n_activities + 1))
        self.durations = self.data.get('dur', [1] * self.n_activities)
        self.precedence_graph = self.data.get('precedence_graph', {})
        
        # Données temporelles (calculées ou fournies)
        self.est = self.data.get('est', [0] * self.n_activities)
        self.lst = self.data.get('lst', [0] * self.n_activities)
        self.lft = self.data.get('lft', [0] * self.n_activities)
        self.eft = [self.est[i] + self.durations[i] for i in range(self.n_activities)]
        
        # Flottement dynamique
        self.float_dyn = self.data.get('float_dyn', [float('inf')] * self.n_activities)
        
        # Utilisation des ressources et compétences
        self.resource_usage = self.data.get('resource_usage', {})
        self.skill_requirements = self.data.get('sreq', [])
        self.resource_mastery = self.data.get('mastery', [])
        
        # Mémoisation pour HRPW
        self.hrpw_memo = {}
        self.successors_memo = {}
        
        # Initialisation
        self._initialize_precedence_graph()
        self._compute_all_metrics()
    
    def _initialize_precedence_graph(self):
        """Initialise le graphe de précédence pour toutes les activités"""
        for activity in self.activities:
            if activity not in self.precedence_graph:
                self.precedence_graph[activity] = {
                    'successors': [],
                    'predecessors': []
                }
    
    def _compute_all_metrics(self):
        """Calcule tous les métriques nécessaires"""
        self._compute_hrpw_all()
        self._compute_resource_metrics()
    
    def _compute_hrpw(self, task: int) -> float:
        """
        Calcule le Highest Rank Positional Weight pour une tâche
        HRPW* = durée + max(HRPW des successeurs)
        """
        if task in self.hrpw_memo:
            return self.hrpw_memo[task]
        
        successors = self.precedence_graph[task]['successors']
        if not successors:
            # Tâche finale
            hrpw_value = self.durations[task - 1]
        else:
            # HRPW = durée + max(HRPW des successeurs)
            hrpw_value = (
                self.durations[task - 1] + 
                max(self._compute_hrpw(succ) for succ in successors)
            )
        
        self.hrpw_memo[task] = hrpw_value
        return hrpw_value
    
    def _compute_hrpw_all(self):
        """Calcule HRPW pour toutes les activités"""
        for task in self.activities:
            self._compute_hrpw(task)
    
    def _count_total_successors(self, task: int) -> int:
        """Compte le nombre total de successeurs (directs et indirects)"""
        if task in self.successors_memo:
            return self.successors_memo[task]
        
        visited = set()
        queue = deque([task])
        total_successors = 0
        
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            
            successors = self.precedence_graph[current]['successors']
            total_successors += len(successors)
            queue.extend(successors)
        
        # Soustraire la tâche elle-même
        total_successors = len(visited) - 1
        self.successors_memo[task] = total_successors
        return total_successors
    
    def _compute_resource_metrics(self):
        """Calcule les métriques liées aux ressources"""
        # S'assurer que resource_usage est un dictionnaire
        if not isinstance(self.resource_usage, dict):
            self.resource_usage = {}
        
        # Si pas de données de ressources, utiliser des valeurs par défaut
        if not self.resource_usage:
            for task in self.activities:
                self.resource_usage[task] = 1
    
    def _get_resource_demand(self, task: int) -> float:
        """Calcule la demande en ressources pour une tâche"""
        if not self.skill_requirements or not self.resource_mastery:
            return self.resource_usage.get(task, 1)
        
        # Calcul basé sur les compétences requises
        if task <= len(self.skill_requirements):
            required_skills = self.skill_requirements[task - 1]
            total_demand = sum(1 for skill in required_skills if skill)
            return max(total_demand, 1)
        
        return self.resource_usage.get(task, 1)
    
    def _get_resource_availability(self, task: int) -> float:
        """Estime la disponibilité des ressources pour une tâche"""
        if not self.resource_mastery or not self.skill_requirements:
            return 1.0
        
        if task > len(self.skill_requirements):
            return 1.0
        
        required_skills = self.skill_requirements[task - 1]
        available_resources = 0
        
        for resource_idx, masteries in enumerate(self.resource_mastery):
            can_do_task = all(
                not required_skills[skill_idx] or masteries[skill_idx]
                for skill_idx in range(len(required_skills))
            )
            if can_do_task:
                available_resources += 1
        
        return max(available_resources, 1)
    
    # Algorithmes de tri
    
    def sort_by_hrpw(self) -> List[int]:
        """HRPW* - Highest Rank Positional Weight"""
        return sorted(
            self.activities,
            key=lambda t: self.hrpw_memo[t],
            reverse=True
        )
    
    def sort_by_lst(self) -> List[int]:
        """LST - Late Start Time"""
        return sorted(
            self.activities,
            key=lambda t: self.lst[t - 1]
        )
    
    def sort_by_lft(self) -> List[int]:
        """LFT - Late Finish Time"""
        return sorted(
            self.activities,
            key=lambda t: self.lft[t - 1]
        )
    
    def sort_by_mts(self) -> List[int]:
        """MTS - Maximum Total Successors"""
        return sorted(
            self.activities,
            key=lambda t: self._count_total_successors(t),
            reverse=True
        )
    
    def sort_by_timros(self) -> List[int]:
        """TIMROS - Time/Resource Availability ratio"""
        ratios = {}
        for task in self.activities:
            duration = self.durations[task - 1]
            availability = self._get_resource_availability(task)
            ratios[task] = (duration / availability
                            if availability > 0 else float('inf'))
        
        return sorted(self.activities, key=lambda t: ratios[t], reverse=True)
    
    def sort_by_hru1(self) -> List[int]:
        """HRU1 - Highest Resource Utilization 1"""
        return sorted(
            self.activities,
            key=lambda t: self._get_resource_demand(t),
            reverse=True
        )
    
    def sort_by_timres(self) -> List[int]:
        """TIMRES - Time * Resource demand"""
        scores = {}
        for task in self.activities:
            duration = self.durations[task - 1]
            demand = self._get_resource_demand(task)
            scores[task] = duration * demand
        
        return sorted(self.activities, key=lambda t: scores[t], reverse=True)
    
    def sort_by_hru2(self) -> List[int]:
        """HRU2 - Resource demand weighted by duration"""
        return sorted(
            self.activities,
            key=lambda t: self._get_resource_demand(t) * self.durations[t - 1],
            reverse=True
        )
    
    def sort_by_stfd(self) -> List[int]:
        """STFD - Smallest Dynamic Total Float"""
        return sorted(
            self.activities,
            key=lambda t: self.float_dyn[t - 1]
        )
    
    def sort_by_eft(self) -> List[int]:
        """EFT - Early Finish Time"""
        return sorted(
            self.activities,
            key=lambda t: self.eft[t - 1]
        )
    
    def _respect_precedence_constraints(self,
                                        ordered_activities: List[int]
                                        ) -> List[int]:
        """
        Réordonne les activités pour respecter les contraintes de précédence
        en utilisant un tri topologique pondéré
        """
        # Créer le graphe NetworkX
        G = nx.DiGraph()
        for activity in self.activities:
            G.add_node(activity)
        
        for activity in self.activities:
            for successor in self.precedence_graph[activity]['successors']:
                G.add_edge(activity, successor)
        
        # Vérifier s'il y a des cycles
        if not nx.is_directed_acyclic_graph(G):
            print("Attention: Cycle détecté dans le graphe de précédence!")
            return ordered_activities
        
        # Créer un dictionnaire de priorités
        priority_map = {act: idx for idx, act in enumerate(ordered_activities)}
        
        # Tri topologique respectant les priorités
        result = []
        remaining = set(ordered_activities)
        
        while remaining:
            # Trouver les tâches prêtes (sans prédécesseurs non traités)
            ready_tasks = [
                task for task in remaining
                if all(pred not in remaining for pred in G.predecessors(task))
            ]
            
            if not ready_tasks:
                # Situation anormale, ajouter les tâches restantes
                result.extend(sorted(remaining))
                break
            
            # Choisir la tâche avec la meilleure priorité
            next_task = min(ready_tasks,
                            key=lambda t: priority_map.get(t, float('inf')))
            result.append(next_task)
            remaining.remove(next_task)
        
        return result
    
    def get_ordered_activities(self, rule_name: str) -> List[int]:
        """
        Retourne les activités ordonnées selon la règle spécifiée
        """
        rule_mapping = {
            'HRPW*': self.sort_by_hrpw,
            'LST': self.sort_by_lst,
            'LFT': self.sort_by_lft,
            'MTS': self.sort_by_mts,
            'TIMROS': self.sort_by_timros,
            'HRU1': self.sort_by_hru1,
            'TIMRES': self.sort_by_timres,
            'HRU2': self.sort_by_hru2,
            'STFD': self.sort_by_stfd,
            'EFT': self.sort_by_eft
        }
        
        if rule_name not in rule_mapping:
            available_rules = ', '.join(rule_mapping.keys())
            raise ValueError(
                f"Règle inconnue: {rule_name}. "
                f"Règles disponibles: {available_rules}"
            )
        
        # Appliquer la règle de tri
        ordered_activities = rule_mapping[rule_name]()
        
        # Respecter les contraintes de précédence
        return self._respect_precedence_constraints(ordered_activities)
    
    def get_all_priority_orders(self) -> Dict[str, List[int]]:
        """Retourne tous les ordres de priorité pour toutes les règles"""
        all_rules = ['HRPW*', 'LST', 'LFT', 'MTS', 'TIMROS',
                     'HRU1', 'TIMRES', 'HRU2', 'STFD', 'EFT']
        results = {}
        
        for rule in all_rules:
            results[rule] = self.get_ordered_activities(rule)
        
        return results


def parse_dzn_file(filepath: str) -> Dict[str, Any]:
    """
    Parse un fichier .dzn et extrait les données d'instance MS-RCPSP
    """
    data = {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as file:
            content = file.read()
    
    # Supprimer les commentaires
    content = re.sub(r'%.*', '', content)
    
    # Parser les variables simples
    simple_patterns = [
        (r'(\w+)\s*=\s*(\d+);', lambda x: int(x)),
        (r'(\w+)\s*=\s*(true|false);', lambda x: x.lower() == 'true'),
        (r'(\w+)\s*=\s*\[([^\]]+)\];',
         lambda x: [int(i) for i in re.findall(r'-?\d+', x)])
    ]
    
    for pattern, converter in simple_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for var_name, var_value in matches:
            try:
                data[var_name] = converter(var_value)
            except (ValueError, TypeError):
                data[var_name] = var_value
    
    # Parser les matrices (sreq, mastery)
    matrix_pattern = r'(\w+)\s*=\s*\[\|(.+?)\|\];'
    matrix_matches = re.findall(matrix_pattern, content, re.DOTALL)
    
    for matrix_name, matrix_content in matrix_matches:
        rows = []
        for row_content in matrix_content.split('|'):
            row_content = row_content.strip()
            if not row_content:
                continue
            
            # Extraire les valeurs (nombres, true, false)
            values = []
            tokens = re.findall(r'\b(?:\d+|true|false)\b',
                                row_content, re.IGNORECASE)
            
            for token in tokens:
                if token.lower() == 'true':
                    values.append(True)
                elif token.lower() == 'false':
                    values.append(False)
                else:
                    values.append(int(token))
            
            if values:
                rows.append(values)
        
        data[matrix_name] = rows
    
    # Construire le graphe de précédence
    precedence_graph = {}
    n_acts = data.get('nActs', 0)
    
    # Initialiser toutes les activités
    for activity in range(1, n_acts + 1):
        precedence_graph[activity] = {'successors': [], 'predecessors': []}
    
    # Ajouter les relations de précédence
    if 'pred' in data and 'succ' in data:
        predecessors = data['pred']
        successors = data['succ']
        
        for pred, succ in zip(predecessors, successors):
            if pred in precedence_graph and succ in precedence_graph:
                precedence_graph[pred]['successors'].append(succ)
                precedence_graph[succ]['predecessors'].append(pred)
    
    data['precedence_graph'] = precedence_graph
    
    return data


def compute_temporal_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule les métriques temporelles (EST, LST, LFT) si elles ne sont pas fournies
    """
    n_acts = data.get('nActs', 0)
    durations = data.get('dur', [1] * n_acts)
    precedence_graph = data.get('precedence_graph', {})
    
    # Calcul EST (Earliest Start Time) - propagation avant
    est = [0] * n_acts
    
    def calculate_est(activity):
        if est[activity - 1] > 0:  # Déjà calculé
            return est[activity - 1]
        
        predecessors = precedence_graph.get(activity, {}).get('predecessors', [])
        if not predecessors:
            est[activity - 1] = 0
        else:
            max_pred_finish = max(
                calculate_est(pred) + durations[pred - 1] 
                for pred in predecessors
            )
            est[activity - 1] = max_pred_finish
        
        return est[activity - 1]
    
    for activity in range(1, n_acts + 1):
        calculate_est(activity)
    
    # Calcul de la durée totale du projet
    project_duration = max(est[i] + durations[i] for i in range(n_acts))
    
    # Calcul LST (Latest Start Time) - propagation arrière
    lst = [project_duration] * n_acts
    lft = [project_duration] * n_acts
    
    def calculate_lst(activity):
        successors = precedence_graph.get(activity, {}).get('successors', [])
        if not successors:
            # Activité finale
            lft[activity - 1] = project_duration
            lst[activity - 1] = project_duration - durations[activity - 1]
        else:
            min_succ_start = min(calculate_lst(succ) for succ in successors)
            lft[activity - 1] = min_succ_start
            lst[activity - 1] = min_succ_start - durations[activity - 1]
        
        return lst[activity - 1]
    
    for activity in range(1, n_acts + 1):
        calculate_lst(activity)
    
    # Calcul du flottement
    float_dyn = [lst[i] - est[i] for i in range(n_acts)]
    
    data['est'] = est
    data['lst'] = lst
    data['lft'] = lft
    data['float_dyn'] = float_dyn
    
    return data


def main():
    """Fonction principale"""
    instances_dir = "./instances"
    results_dir = "./resultats"
    
    # Créer le répertoire de résultats
    os.makedirs(results_dir, exist_ok=True)
    
    # Trouver tous les fichiers .dzn
    dzn_files = glob.glob(os.path.join(instances_dir, "*.dzn"))
    
    if not dzn_files:
        print(f"Aucune instance .dzn trouvée dans {instances_dir}")
        return
    
    print(f"Trouvé {len(dzn_files)} instance(s) à traiter.")
    
    # Traiter chaque instance
    for dzn_file in dzn_files:
        instance_name = os.path.splitext(os.path.basename(dzn_file))[0]
        print(f"\n{'='*50}")
        print(f"Traitement de l'instance: {instance_name}")
        print(f"{'='*50}")
        
        try:
            # Charger et parser l'instance
            instance_data = parse_dzn_file(dzn_file)
            
            # Calculer les métriques temporelles si nécessaires
            instance_data = compute_temporal_metrics(instance_data)
            
            # Créer l'objet algorithmes
            algorithms = MSRCPSPPriorityAlgorithms(instance_data)
            
            # Obtenir tous les ordres de priorité
            all_orders = algorithms.get_all_priority_orders()
            
            # Sauvegarder les résultats pour chaque règle
            for rule_name, activity_order in all_orders.items():
                # Créer le répertoire pour cette règle
                rule_dir = os.path.join(results_dir, rule_name)
                os.makedirs(rule_dir, exist_ok=True)
                
                # Préparer les données de sortie
                output_data = {
                    "instance": instance_name,
                    "rule": rule_name,
                    "n_activities": instance_data.get('nActs', 0),
                    "n_resources": instance_data.get('nRes', 0),
                    "n_skills": instance_data.get('nSkills', 0),
                    "ordered_activities": activity_order,
                    "durations": instance_data.get('dur', []),
                    "est": instance_data.get('est', []),
                    "lst": instance_data.get('lst', []),
                    "lft": instance_data.get('lft', []),
                    "hrpw_values": {
                        str(task): algorithms.hrpw_memo.get(task, 0) 
                        for task in algorithms.activities
                    }
                }
                
                # Sauvegarder dans un fichier JSON
                output_file = os.path.join(rule_dir, f"{instance_name}.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                
                print(f"  {rule_name}: {activity_order[:10]}{'...' if len(activity_order) > 10 else ''}")
            
            print(f"\nRésultats sauvegardés dans {results_dir}")
            
        except Exception as e:
            print(f"Erreur lors du traitement de {instance_name}: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()