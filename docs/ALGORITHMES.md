# 📊 Algorithmes d'Ordonnancement MS-RCPSP

## 📋 Vue d'ensemble

Le système MS-RCPSP implémente **7 algorithmes d'ordonnancement** différents, chacun avec sa propre stratégie pour résoudre les problèmes de planification de projets avec contraintes de ressources et compétences multiples.

## 🎯 Principe général MS-RCPSP

### **Contraintes du problème**
- **Précédences** : Certaines tâches doivent être terminées avant d'autres
- **Ressources limitées** : Capacités fixes pour chaque type de ressource
- **Compétences multiples** : Chaque tâche requiert des compétences spécifiques
- **Disponibilité ressources** : Les ressources ont des compétences variables

### **Objectif**
Minimiser le **makespan** (durée totale du projet) tout en respectant toutes les contraintes.

## 🔧 Algorithmes implémentés

### 1. 🕐 **EST - Earliest Start Time**

#### **Principe**
Ordonne les tâches par leur **date de début au plus tôt** possible.

#### **Algorithme**
```python
def est_priority(job, current_time, completed_jobs):
    """Calcule la priorité EST"""
    
    # Date de début au plus tôt = fin des prédécesseurs
    earliest_start = 0
    for pred in job.predecessors:
        if pred in completed_jobs:
            earliest_start = max(earliest_start, 
                                completed_jobs[pred].finish_time)
    
    return earliest_start
```

#### **Avantages**
- ✅ Intuitive et naturelle
- ✅ Respecte l'ordre logique des précédences
- ✅ Souvent optimal pour projets séquentiels

#### **Inconvénients**
- ❌ Ne considère pas la disponibilité des ressources
- ❌ Peut créer des goulots d'étranglement

#### **Quand l'utiliser**
- Projets avec forte contrainte temporelle
- Peu de concurrence sur les ressources
- Précédences critiques importantes

---

### 2. 🕑 **LFT - Latest Finish Time**

#### **Principe**
Ordonne les tâches par leur **date de fin au plus tard** (backward scheduling).

#### **Algorithme**
```python
def lft_priority(job, project_deadline):
    """Calcule la priorité LFT"""
    
    # Date de fin au plus tard = deadline - successeurs
    latest_finish = project_deadline
    for succ in job.successors:
        latest_finish = min(latest_finish,
                           succ.latest_start - succ.duration)
    
    return -latest_finish  # Ordre croissant
```

#### **Avantages**
- ✅ Identifie les tâches critiques
- ✅ Évite les retards en cascade
- ✅ Bon pour projets avec deadline fixe

#### **Inconvénients**
- ❌ Nécessite connaissance de la deadline
- ❌ Peut sous-utiliser les ressources

#### **Quand l'utiliser**
- Projets avec deadline stricte
- Tâches critiques identifiées
- Optimisation de la fin de projet

---

### 3. 🎯 **MSLF - Most Skills Last First**

#### **Principe**
Privilégie les tâches nécessitant le **plus de compétences** en dernier.

#### **Algorithme**
```python
def mslf_priority(job):
    """Calcule la priorité MSLF"""
    
    # Nombre de compétences requises
    num_skills = len(job.required_skills)
    
    # Plus de compétences = priorité plus faible
    return -num_skills
```

#### **Avantages**
- ✅ Optimise l'utilisation des ressources qualifiées
- ✅ Évite les blocages sur compétences rares
- ✅ Bon pour projets multi-compétences

#### **Inconvénients**
- ❌ Peut ignorer les précédences
- ❌ Sous-optimal si compétences bien distribuées

#### **Quand l'utiliser**
- Ressources avec compétences spécialisées
- Compétences rares et critiques
- Projets nécessitant coordination expertise

---

### 4. ⚡ **SPT - Shortest Processing Time**

#### **Principe**
Ordonne les tâches par **durée croissante** (tâches courtes en premier).

#### **Algorithme**
```python
def spt_priority(job):
    """Calcule la priorité SPT"""
    
    # Durée de la tâche
    return job.duration
```

#### **Avantages**
- ✅ Maximise le nombre de tâches terminées rapidement
- ✅ Réduit le temps d'attente moyen
- ✅ Simple et efficace

#### **Inconvénients**
- ❌ Peut retarder les tâches longues importantes
- ❌ Ignore les contraintes de ressources

#### **Quand l'utiliser**
- Optimisation du nombre de tâches finies
- Projets avec beaucoup de petites tâches
- Minimisation du temps de cycle

---

### 5. 🔄 **LPT - Longest Processing Time**

#### **Principe**
Ordonne les tâches par **durée décroissante** (tâches longues en premier).

#### **Algorithme**
```python
def lpt_priority(job):
    """Calcule la priorité LPT"""
    
    # Durée négative pour ordre décroissant
    return -job.duration
```

#### **Avantages**
- ✅ Traite les tâches critiques en premier
- ✅ Évite les retards sur tâches importantes
- ✅ Parallélise mieux les tâches longues

#### **Inconvénients**
- ❌ Peut bloquer les ressources longtemps
- ❌ Retarde les tâches courtes

#### **Quand l'utiliser**
- Tâches longues sur le chemin critique
- Ressources abondantes
- Optimisation du makespan global

---

### 6. 📋 **FCFS - First Come First Served**

#### **Principe**
Ordonne les tâches par **ordre d'arrivée** ou d'apparition dans le fichier.

#### **Algorithme**
```python
def fcfs_priority(job, job_list):
    """Calcule la priorité FCFS"""
    
    # Index dans la liste originale
    return job_list.index(job)
```

#### **Avantages**
- ✅ Équitable et prévisible
- ✅ Simple à implémenter
- ✅ Aucun calcul complexe

#### **Inconvénients**
- ❌ Généralement sous-optimal
- ❌ Ignore toutes les contraintes spécifiques
- ❌ Peut créer des inefficacités

#### **Quand l'utiliser**
- Référence de comparaison
- Contraintes d'équité strictes
- Situations d'incertitude totale

---

### 7. ⏰ **LST - Latest Start Time**

#### **Principe**
Ordonne les tâches par leur **date de début au plus tard**.

#### **Algorithme**
```python
def lst_priority(job, project_deadline):
    """Calcule la priorité LST"""
    
    # Date de début au plus tard
    latest_start = project_deadline
    for succ in job.successors:
        latest_start = min(latest_start,
                          succ.latest_start - job.duration)
    
    return latest_start
```

#### **Avantages**
- ✅ Identifie les tâches les plus urgentes
- ✅ Optimise l'utilisation du temps disponible
- ✅ Équilibre précédences et ressources

#### **Inconvénients**
- ❌ Complexe à calculer
- ❌ Nécessite estimation de durée projet

#### **Quand l'utiliser**
- Projets avec slack temporel important
- Optimisation fine des délais
- Gestion des priorités dynamiques

## 📊 Comparaison des performances

### **Résultats statistiques (sur 20 instances)**

| Algorithme | Victoires | % Optimal | Makespan Moyen | Écart type |
|------------|-----------|-----------|----------------|------------|
| **EST**    | 4         | 20%       | 89.2 jours     | 35.8       |
| **LPT**    | 8         | 40%       | 88.7 jours     | 35.4       |
| **LST**    | 8         | 40%       | 89.1 jours     | 35.7       |
| **SPT**    | 2         | 10%       | 89.8 jours     | 36.1       |
| **LFT**    | 1         | 5%        | 90.3 jours     | 36.3       |
| **MSLF**   | 0         | 0%        | 90.8 jours     | 36.5       |
| **FCFS**   | 0         | 0%        | 91.1 jours     | 36.7       |

### **Patterns observés**

#### **LPT & LST dominants**
- **40% des victoires chacun**
- Excellents sur projets avec tâches longues critiques
- Gestion efficace des ressources limitées

#### **EST polyvalent**
- **20% des victoires**
- Bon compromis général
- Efficace sur projets séquentiels

#### **SPT spécialisé**
- Optimal sur projets avec nombreuses tâches courtes
- Moins efficace sur projets déséquilibrés

#### **Algorithmes de référence**
- **FCFS** : Toujours sous-optimal (référence)
- **MSLF** : Efficace seulement si compétences très critiques

## 🎯 Recommandations d'utilisation

### **Selon le type de projet**

#### **Projets industriels (construction, manufacture)**
1. **LPT** - Tâches longues critiques
2. **EST** - Respect des précédences
3. **LST** - Optimisation des délais

#### **Projets logiciels (développement, tests)**
1. **SPT** - Nombreuses petites tâches
2. **EST** - Dépendances entre modules
3. **LFT** - Deadlines de livraison

#### **Projets R&D (recherche, innovation)**
1. **MSLF** - Expertise spécialisée critique
2. **LST** - Incertitudes sur durées
3. **LPT** - Phases longues d'expérimentation

### **Selon les contraintes**

#### **Ressources très limitées**
```
1. LST  - Optimise l'utilisation temporelle
2. MSLF - Gère les compétences rares
3. LPT  - Traite les priorités en premier
```

#### **Deadline stricte**
```
1. LFT  - Planification inverse
2. EST  - Démarrage rapide
3. LST  - Équilibre urgence/ressources
```

#### **Précédences complexes**
```
1. EST  - Respect naturel des dépendances
2. LFT  - Identification du chemin critique
3. LST  - Optimisation des marges
```

## 🔧 Implémentation technique

### **Structure commune**
```python
class PriorityRule:
    def __init__(self, name):
        self.name = name
    
    def calculate_priority(self, job, context):
        """Calcule la priorité de la tâche"""
        raise NotImplementedError
    
    def schedule(self, jobs, resources, precedences):
        """Exécute l'ordonnancement complet"""
        
        # 1. Initialiser
        scheduled_jobs = []
        ready_jobs = get_ready_jobs(jobs, precedences)
        current_time = 0
        
        # 2. Boucle principale
        while ready_jobs or has_running_jobs():
            
            # Calculer priorités
            priorities = {}
            for job in ready_jobs:
                priorities[job] = self.calculate_priority(job, context)
            
            # Trier par priorité
            sorted_jobs = sorted(ready_jobs, key=lambda j: priorities[j])
            
            # Ordonnancer le premier disponible
            for job in sorted_jobs:
                if can_schedule(job, resources, current_time):
                    schedule_job(job, current_time)
                    break
            
            # Avancer le temps
            current_time = next_event_time()
        
        return calculate_makespan(scheduled_jobs)
```

### **Optimisations implémentées**

#### **Gestion efficace des ressources**
```python
def check_resource_availability(job, resources, start_time):
    """Vérifie la disponibilité des ressources"""
    
    for skill in job.required_skills:
        available_resources = [r for r in resources 
                              if skill in r.skills 
                              and r.is_available(start_time, job.duration)]
        
        if not available_resources:
            return False, None
    
    return True, selected_resources
```

#### **Calcul incrémental des priorités**
```python
def update_priorities_incremental(jobs, last_event):
    """Met à jour seulement les priorités affectées"""
    
    for job in jobs:
        if job.affected_by(last_event):
            job.priority = calculate_priority(job)
```

#### **Cache des calculs coûteux**
```python
@lru_cache(maxsize=1000)
def calculate_latest_start_time(job_id, deadline):
    """Cache les calculs LST coûteux"""
    return compute_lst(job_id, deadline)
```

## 📈 Métriques de performance

### **Makespan (objectif principal)**
```python
def calculate_makespan(scheduled_jobs):
    """Calcule la durée totale du projet"""
    return max(job.finish_time for job in scheduled_jobs)
```

### **Utilisation des ressources**
```python
def resource_utilization(schedule, resources):
    """Calcule le taux d'utilisation des ressources"""
    total_capacity = sum(r.capacity for r in resources)
    used_capacity = calculate_used_capacity(schedule)
    return used_capacity / total_capacity
```

### **Respect des contraintes**
```python
def validate_schedule(schedule, precedences, resources):
    """Valide que toutes les contraintes sont respectées"""
    
    # Vérifier précédences
    for job in schedule:
        for pred in job.predecessors:
            assert pred.finish_time <= job.start_time
    
    # Vérifier ressources
    for time_slot in schedule.time_slots:
        assert not resource_overload(time_slot, resources)
    
    return True
```

## 🎯 Évolutions futures

### **Algorithmes hybrides**
- **Combinaison EST+LPT** : Démarrage rapide + tâches longues
- **SPT adaptatif** : Ajustement selon disponibilité ressources
- **LST avec relaxation** : Tolérance sur estimations durées

### **Optimisations avancées**
- **Algorithmes génétiques** : Exploration de l'espace de solutions
- **Simulated annealing** : Amélioration locale
- **Branch and bound** : Solutions exactes sur petites instances

### **Adaptation temps réel**
- **Priorités dynamiques** : Ajustement selon événements
- **Réordonnancement** : Adaptation aux imprévus
- **Apprentissage en ligne** : Amélioration continue des heuristiques
