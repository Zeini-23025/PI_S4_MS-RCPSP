# 🏆 Algorithmes de Priorité pour MSRCPSP

Ce document détaille les **9 algorithmes de priorité** implémentés pour résoudre le problème MSRCPSP. Chaque algorithme utilise une stratégie différente pour ordonner les activités et optimiser le makespan.

---

## 🎯 Principe Général

Les **règles de priorité** sont des heuristiques qui :
1. **Classent** les activités prêtes à être exécutées
2. **Sélectionnent** la prochaine activité à ordonnancer
3. **Assignent** les ressources disponibles et compétentes
4. **Répètent** le processus jusqu'à la fin du projet

---

## 📋 Top 10 Règles de Priorité

## 1. **MSLF (Minimum Slack Time)** ⏰
- **Formule :** `LFT - EST - Duration`
- **Principe :** Priorise les activités avec la plus petite marge de flexibilité
- **Avantages :** Excellent pour éviter les goulots d'étranglement dans les projets multi-compétences
- **Performance :** ⭐⭐⭐⭐⭐

## 2. **MCS (Most Critical Successor)** 🔗
- **Formule :** `Somme des criticités des successeurs directs`
- **Principe :** Priorise les activités ayant le plus de tâches critiques en aval
- **Avantages :** Maintient la fluidité du projet en libérant les ressources critiques
- **Performance :** ⭐⭐⭐⭐⭐

## 3. **LFT (Latest Finish Time)** 📅
- **Formule :** `Temps de fin au plus tard`
- **Principe :** Priorise les activités devant se terminer le plus tôt
- **Avantages :** Réduit les risques de dépassement de délais
- **Performance :** ⭐⭐⭐⭐⭐

## 4. **GRASP-Based Priority** 🎯
- **Formule :** `Combinaison adaptative de plusieurs règles`
- **Principe :** Sélection intelligente basée sur la criticité et disponibilité des ressources
- **Avantages :** S'adapte dynamiquement aux contraintes multi-compétences
- **Performance :** ⭐⭐⭐⭐⭐

## 5. **EST (Earliest Start Time)** 🚀
- **Formule :** `Temps de début au plus tôt`
- **Principe :** Priorise les activités pouvant commencer immédiatement
- **Avantages :** Maximise l'utilisation des ressources disponibles
- **Performance :** ⭐⭐⭐⭐

## 6. **SPT (Shortest Processing Time)** ⚡
- **Formule :** `Durée minimale`
- **Principe :** Priorise les activités les plus courtes
- **Avantages :** Augmente rapidement le nombre de tâches terminées
- **Performance :** ⭐⭐⭐⭐

## 7. **MRD (Maximum Resource Demand)** 💪
- **Formule :** `Nombre total de ressources requises`
- **Principe :** Priorise les activités nécessitant le plus de ressources
- **Avantages :** Évite les conflits d'allocation en traitant les tâches lourdes en premier
- **Performance :** ⭐⭐⭐

## 8. **MSC (Minimum Skilled Combinations)** 🔧
- **Formule :** `Nombre de combinaisons de compétences valides`
- **Principe :** Priorise les activités avec peu d'options d'assignation
- **Avantages :** Évite les blocages dus aux contraintes de compétences
- **Performance :** ⭐⭐⭐⭐

## 9. **MSLR (Maximum Skill Level Requirement)** 🎓
- **Formule :** `Niveau de compétence maximal requis`
- **Principe :** Priorise les activités nécessitant des compétences élevées
- **Avantages :** Utilise efficacement les ressources hautement qualifiées
- **Performance :** ⭐⭐⭐

## 10. **MTS (Most Total Successors)** 🌐
- **Formule :** `Nombre total de successeurs directs et indirects`
- **Principe :** Priorise les activités ayant le plus de dépendances
- **Avantages :** Maintient la continuité du flux de travail
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

## 📊 Comparaison des Performances

| Algorithme | Complexité | Efficacité Temps | Gestion Ressources | Adaptabilité |
|------------|------------|------------------|-------------------|--------------|
| **MSLF** | O(n) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **LFT** | O(n) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **MCS** | O(n²) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **EST** | O(n) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **SPT** | O(n log n) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **MSC** | O(n×m) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **MRD** | O(n) | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **MSLR** | O(n) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **MTS** | O(n²) | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

*n = nombre d'activités, m = nombre de ressources*

---

## 🎓 Conseils d'Utilisation

### Pour Projets Courts (< 20 activités)
- **Recommandé :** MSLF, LFT, EST
- **Éviter :** MCS, MTS (overhead de calcul)

### Pour Projets avec Contraintes de Compétences Élevées
- **Recommandé :** MSC, MSLR, MCS
- **Éviter :** SPT, MRD (ignorent les compétences)

### Pour Projets avec Ressources Limitées
- **Recommandé :** MRD, EST, MSC
- **Éviter :** SPT (peut créer des conflits)

### Pour Projets avec Échéances Serrées
- **Recommandé :** MSLF, LFT, MCS
- **Éviter :** MRD, MTS (moins orientés temps)

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
