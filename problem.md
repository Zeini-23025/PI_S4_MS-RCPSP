# 🎯 Problème MSRCPSP - Description Complète

## 📝 Définition

Le **MSRCPSP** (Multi-Skilled Resource-Constrained Project Scheduling Problem) est un problème d'optimisation combinatoire qui étend le RCPSP classique en incluant la gestion des compétences multiples des ressources humaines.

---

## 🧩 Composants du Problème

### 1. **Activités du Projet**
- **Durée fixe** : Chaque activité a une durée déterministe
- **Dépendances** : Relations de précédence entre activités
- **Exigences** : Compétences et niveaux requis pour l'exécution

### 2. **Ressources Humaines**  
- **Multi-compétentes** : Chaque ressource maîtrise plusieurs compétences
- **Niveaux variables** : Différents niveaux de maîtrise (1-5)
- **Disponibilité** : Une ressource ne peut travailler que sur une activité à la fois

### 3. **Compétences**
- **Types multiples** : Programmation, Test, Gestion, Design, etc.
- **Niveaux requis** : Chaque activité spécifie le niveau minimal nécessaire
- **Contraintes strictes** : Une activité ne peut commencer sans les compétences requises

---

## 🎯 Objectif d'Optimisation

**Minimiser le makespan** : Durée totale du projet (temps entre début et fin)

```
Makespan = max(temps_fin_activité) - min(temps_début_activité)
```

---

## 🔗 Contraintes Principales

### 1. **Contraintes de Précédence**
```
∀ activité j, ∀ prédécesseur i : temps_début[j] ≥ temps_fin[i]
```

### 2. **Contraintes de Ressources**
```
∀ ressource r, ∀ temps t : 
  nombre_activités_assignées[r,t] ≤ 1
```

### 3. **Contraintes de Compétences**
```
∀ activité j, ∀ compétence s :
  nombre_ressources_affectées[j,s] ≥ exigence[j,s]
  niveau_ressource[r,s] ≥ niveau_requis[j,s]
```

---

## 📊 Modèle Mathématique

### Variables de Décision
- **xijt** : Binaire, 1 si l'activité j commence au temps t avec la ressource i
- **yij** : Binaire, 1 si la ressource i est assignée à l'activité j

### Fonction Objectif
```
Minimiser : Cmax = max(t + dj) × xijt
```

### Contraintes Principales
```
1. Précédence : ∑t×xijt + dj ≤ ∑t×xi'j't   ∀(j,j') ∈ A

2. Ressources : ∑j yij ≤ 1   ∀i, ∀t

3. Compétences : ∑i (skills[i,s] × yij) ≥ req[j,s]   ∀j, ∀s

4. Niveaux : level[i,s] ≥ req_level[j,s] × yij   ∀i, ∀j, ∀s
```

---

## 💡 Exemple Concret

### Projet de Développement Logiciel

#### Activités :
1. **Analyse** (5 jours) → Gestion niveau 3
2. **Design** (3 jours) → Design niveau 4  
3. **Codage** (7 jours) → Programmation niveau 3
4. **Tests** (4 jours) → Test niveau 2
5. **Déploiement** (2 jours) → Gestion niveau 4, Technique niveau 3

#### Ressources :
- **Alice** : Gestion(5), Design(2), Programmation(1), Test(3)
- **Bob** : Programmation(5), Test(4), Gestion(2), Design(3)  
- **Charlie** : Test(5), Gestion(3), Programmation(2), Design(4)

#### Dépendances :
Analyse → Design → Codage → Tests → Déploiement

#### Solution Optimale :
```
Temps 0-5  : Alice fait Analyse
Temps 5-8  : Charlie fait Design  
Temps 8-15 : Bob fait Codage
Temps 15-19: Charlie fait Tests
Temps 19-21: Alice fait Déploiement
Makespan = 21 jours
```

---

## 🔬 Complexité du Problème

### Classe de Complexité
- **NP-Difficile** : Pas d'algorithme polynomial connu
- **Extension du RCPSP** : Déjà NP-difficile
- **Facteurs aggravants** : Compétences multiples, niveaux, assignations

### Méthodes de Résolution
1. **Heuristiques** : Règles de priorité (rapides mais approximatives)
2. **Métaheuristiques** : Algorithmes génétiques, recuit simulé  
3. **Méthodes exactes** : Programmation linéaire en nombres entiers
4. **Approches hybrides** : Combinaison de plusieurs techniques

---

## 📈 Applications Réelles

### Secteurs d'Application
- **Développement logiciel** : Équipes avec compétences diverses
- **Consulting** : Projets clients avec experts spécialisés
- **R&D** : Projets de recherche interdisciplinaires
- **Construction** : Corps de métiers multiples
- **Production** : Lignes avec opérateurs polyvalents

### Bénéfices de l'Optimisation
- **Réduction des délais** : Jusqu'à 15-30% d'amélioration
- **Meilleure utilisation** : Optimisation des compétences rares
- **Flexibilité** : Adaptation aux changements d'équipe
- **Coûts maîtrisés** : Éviter les retards et pénalités

---

## 🛠️ Défis de Résolution

### Défis Algorithmiques
- **Explosion combinatoire** : Nombre de solutions possibles
- **Contraintes complexes** : Interactions entre compétences et temps
- **Qualité vs Temps** : Trade-off entre optimalité et rapidité

### Défis Pratiques  
- **Données incertaines** : Durées et disponibilités variables
- **Changements dynamiques** : Modifications en cours de projet
- **Préférences humaines** : Affinités et conflits dans les équipes
- **Compétences évolutives** : Apprentissage et formation continue

---

## 🚀 Comment Utiliser Notre Solver

1. **Préparez vos données** au format `.msrcp` (voir `instances.md`)
2. **Exécutez le solver** : `python3 msrcpsp_solver.py`
3. **Analysez les résultats** dans le répertoire `resultats/`
4. **Comparez les algorithmes** selon vos critères de performance

Le solver teste automatiquement 9 algorithmes de priorité différents et vous aide à identifier la meilleure stratégie pour votre type de projet !
