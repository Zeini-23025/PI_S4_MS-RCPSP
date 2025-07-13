# 🏆 Algorithmes de Priorité pour MSRCPSP

Ce document détaille les **7 algorithmes de priorité** implémentés pour résoudre le problème MSRCPSP. Chaque algorithme utilise une stratégie différente pour ordonner les activités et optimiser le makespan.

---

## 🎯 Principe Général

Les **règles de priorité** sont des heuristiques qui :
1. **Classent** les activités prêtes à être exécutées
2. **Sélectionnent** la prochaine activité à ordonnancer
3. **Assignent** les ressources disponibles et compétentes
4. **Répètent** le processus jusqu'à la fin du projet

---

## 📋 Les 7 Algorithmes Implémentés

## 1. **EST (Earliest Start Time)** 🚀
- **Formule :** `Temps de début au plus tôt`
- **Principe :** Priorise les activités pouvant commencer immédiatement
- **Stratégie :** Tri croissant par earliest_start
- **Avantages :** Maximise l'utilisation des ressources disponibles
- **Performance :** ⭐⭐⭐⭐

## 2. **LFT (Latest Finish Time)** 📅
- **Formule :** `Temps de fin au plus tard`
- **Principe :** Priorise les activités devant se terminer le plus tôt
- **Stratégie :** Tri croissant par latest_finish
- **Avantages :** Réduit les risques de dépassement de délais
- **Performance :** ⭐⭐⭐⭐⭐

## 3. **MSLF (Minimum Slack Time)** ⏰
- **Formule :** `LFT - EST - Duration = marge de flexibilité`
- **Principe :** Priorise les activités avec la plus petite marge de flexibilité
- **Stratégie :** Tri croissant par slack (marge)
- **Avantages :** Excellent pour éviter les goulots d'étranglement
- **Performance :** ⭐⭐⭐⭐⭐

## 4. **SPT (Shortest Processing Time)** ⚡
- **Formule :** `Durée minimale`
- **Principe :** Priorise les activités les plus courtes
- **Stratégie :** Tri croissant par duration
- **Avantages :** Augmente rapidement le nombre de tâches terminées
- **Performance :** ⭐⭐⭐⭐

## 5. **LPT (Longest Processing Time)** �
- **Formule :** `Durée maximale`
- **Principe :** Priorise les activités les plus longues
- **Stratégie :** Tri décroissant par duration
- **Avantages :** Traite les tâches lourdes tôt pour éviter les retards
- **Performance :** ⭐⭐⭐

## 6. **FCFS (First Come First Served)** �
- **Formule :** `Ordre d'arrivée des activités`
- **Principe :** Priorise les activités dans l'ordre de leur ID
- **Stratégie :** Tri croissant par ID d'activité
- **Avantages :** Simple et équitable, bon pour comparaison baseline
- **Performance :** ⭐⭐

## 7. **LST (Latest Start Time)** ⏳
- **Formule :** `Temps de début au plus tard`
- **Principe :** Priorise les activités devant commencer le plus tard
- **Stratégie :** Tri décroissant par latest_start
- **Avantages :** Utilise la flexibilité temporelle pour optimiser les ressources
- **Performance :** ⭐⭐⭐

---

## 🧮 Formules Détaillées

### 1. MSLF - Minimum Slack Time
```python
slack = latest_start - earliest_start
priority = min(slack)  # Plus petit slack = plus haute priorité
```
**Utilisation :** Identifie les activités sur le chemin critique

### 2. LFT - Latest Finish Time  
```python
priority = latest_finish_time  # Plus petit LFT = plus haute priorité
```
**Utilisation :** Évite les retards en priorisant les échéances urgentes

### 3. MCS - Most Critical Successor
```python
criticality = sum(1/max(successor.slack, 1) for successor in direct_successors)
priority = max(criticality)  # Plus haute criticité = plus haute priorité
```
**Utilisation :** Libère rapidement les activités en aval

### 4. EST - Earliest Start Time
```python
priority = min(earliest_start)  # Plus petit EST = plus haute priorité
```
**Utilisation :** Maximise l'utilisation des ressources disponibles

### 5. SPT - Shortest Processing Time
```python
priority = min(duration)  # Plus courte durée = plus haute priorité
```
**Utilisation :** Termine rapidement de nombreuses tâches

### 6. MSC - Minimum Skilled Combinations
```python
valid_resources = count_compatible_resources(activity)
priority = min(valid_resources)  # Moins d'options = plus haute priorité
```
**Utilisation :** Évite les blocages dus aux contraintes de compétences

### 7. MRD - Maximum Resource Demand
```python
demand = sum(skill_requirements)
priority = max(demand)  # Plus de ressources = plus haute priorité
```
**Utilisation :** Traite les tâches lourdes en premier

### 8. MSLR - Maximum Skill Level Requirement
```python
max_level = max(skill_level_requirements)
priority = max(max_level)  # Niveau plus élevé = plus haute priorité
```
**Utilisation :** Utilise efficacement les ressources hautement qualifiées

### 9. MTS - Most Total Successors
```python
total_successors = count_all_successors_recursive(activity)
priority = max(total_successors)  # Plus de successeurs = plus haute priorité
```
**Utilisation :** Maintient la fluidité du projet

---

## ⚡ Algorithmes Adaptatifs

### GRASP-Based Priority (Concept Avancé)
```python
def grasp_priority(activities, resources, alpha=0.3):
    scores = {}
    for activity in activities:
        # Combinaison de plusieurs critères
        time_score = normalize(activity.slack)
        resource_score = normalize(count_available_resources(activity))
        successor_score = normalize(activity.successor_criticality)
        
        # Score composite
        scores[activity] = (
            0.4 * time_score + 
            0.3 * resource_score + 
            0.3 * successor_score
        )
    
    # Construction de liste restreinte de candidats (RCL)
    best_score = max(scores.values())
    threshold = best_score - alpha * (best_score - min(scores.values()))
    
    candidates = [act for act, score in scores.items() if score >= threshold]
    return random.choice(candidates)  # Sélection aléatoire dans RCL
```

---

## 🔄 Comparaison Pratique des Algorithmes

### Tableau de Performance
| Algorithme | Complexité | Efficacité | Usage Recommandé |
|------------|------------|------------|------------------|
| **MSLF** | O(n log n) | ⭐⭐⭐⭐⭐ | Projets avec contraintes temporelles serrées |
| **LFT** | O(n log n) | ⭐⭐⭐⭐⭐ | Projets avec échéances multiples |
| **EST** | O(n log n) | ⭐⭐⭐⭐ | Maximisation d'utilisation des ressources |
| **SPT** | O(n log n) | ⭐⭐⭐⭐ | Projets avec beaucoup de petites tâches |
| **LPT** | O(n log n) | ⭐⭐⭐ | Projets avec quelques tâches lourdes |
| **LST** | O(n log n) | ⭐⭐⭐ | Optimisation fine de l'ordonnancement |
| **FCFS** | O(n) | ⭐⭐ | Baseline simple et équitable |

### Formules Mathématiques

#### 1. EST (Earliest Start Time)
```python
priority = earliest_start_time  # Plus petit EST = plus haute priorité
```
**Formule :** `EST(i) = max(EFT(j)) pour j ∈ predecessors(i)`

#### 2. LFT (Latest Finish Time)
```python
priority = latest_finish_time  # Plus petit LFT = plus haute priorité
```
**Formule :** `LFT(i) = min(LST(j)) pour j ∈ successors(i)`

#### 3. MSLF (Minimum Slack Time)
```python
priority = slack_time  # Plus petit slack = plus haute priorité
```
**Formule :** `Slack(i) = LST(i) - EST(i) = LFT(i) - EFT(i)`

#### 4. SPT (Shortest Processing Time)
```python
priority = duration  # Plus courte durée = plus haute priorité
```
**Formule :** `SPT(i) = duration(i)`

#### 5. LPT (Longest Processing Time)
```python
priority = -duration  # Plus longue durée = plus haute priorité
```
**Formule :** `LPT(i) = -duration(i)`

#### 6. LST (Latest Start Time)
```python
priority = -latest_start_time  # Plus grand LST = plus haute priorité
```
**Formule :** `LST(i) = LFT(i) - duration(i)`

#### 7. FCFS (First Come First Served)
```python
priority = activity_id  # Plus petit ID = plus haute priorité
```
**Formule :** `FCFS(i) = id(i)`

---

## 📊 Résultats Expérimentaux

### Exemple sur Instance MSLIB_Set1_1
```csv
Algorithme,Makespan,Amélioration vs FCFS
MSLF,35,-12.5%
LFT,40,0%
EST,36,-10%
SPT,36,-10%
LPT,42,+5%
LST,38,-5%
FCFS,40,baseline
```

### Tendances Observées
1. **MSLF** et **LFT** sont généralement les plus performants
2. **EST** offre un bon équilibre entre performance et simplicité
3. **SPT** excelle sur les projets avec beaucoup d'activités courtes
4. **LPT** peut être meilleur quand les ressources sont limitées
5. **LST** fournit des solutions alternatives intéressantes
6. **FCFS** sert de référence baseline

---

## 🎯 Guide de Sélection d'Algorithme

### Selon le Type de Projet
- **Projets urgents** → MSLF ou LFT
- **Ressources limitées** → EST ou LPT
- **Nombreuses petites tâches** → SPT
- **Optimisation fine** → LST
- **Test baseline** → FCFS

### Selon les Contraintes
- **Échéances multiples** → LFT
- **Goulots d'étranglement** → MSLF
- **Utilisation maximale** → EST
- **Équilibrage de charge** → LPT

---

## 🔬 Implémentation dans le Code

Chaque algorithme est implémenté comme une fonction pure dans la classe `PriorityRules` :

```python
@staticmethod
def minimum_slack(activities: List[Activity], current_time: int) -> List[int]:
    """MSLF - Minimum Slack Time"""
    available = [a for a in activities if a.earliest_start <= current_time]
    return sorted([a.id for a in available], key=lambda aid: activities[aid].slack)
```

**Usage dans le scheduler :**
```python
scheduler = MSRCPSPScheduler(instance)
makespan, schedule = scheduler.schedule_with_priority_rule(
    PriorityRules.minimum_slack
)
```
