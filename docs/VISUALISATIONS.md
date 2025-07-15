# 📈 Visualisations et Graphiques

## 📋 Vue d'ensemble

Le système MS-RCPSP génère automatiquement des **visualisations interactives** pour analyser les performances des algorithmes d'ordonnancement et de l'intelligence artificielle.

## 🎨 Scripts de visualisation

### **1. `nettoyage_et_graphiques.py` - Générateur principal**
```bash
python3 nettoyage_et_graphiques.py
```

**Menu disponible** :
```
1. 🧹 Supprimer fichiers non nécessaires
2. 📊 Créer graphiques makespan  
3. 🤖 Créer graphiques ML
4. 🎯 Tout faire (recommandé)
```

### **2. `detail_resultat_ml.py` - Analyse avancée**
```bash
python3 detail_resultat_ml.py
```

**Options** :
```
1️⃣  Analyser un résultat spécifique avec graphiques
2️⃣  Comparer plusieurs résultats avec graphiques
```

## 📊 Types de graphiques générés

### **1. Analyse des Makespans**

#### **📁 Fichier** : `resultats/graphiques/analyse_makespan.png`

**Contient 4 graphiques** :

##### **A. Performance moyenne par algorithme (Barres)**
- **Axe X** : Algorithmes (EST, LFT, MSLF, SPT, LPT, FCFS, LST)
- **Axe Y** : Makespan moyen (jours)
- **Couleurs** : Palette viridis pour distinction
- **Valeurs** : Affichées sur chaque barre

**Interprétation** :
```
Barres basses = Algorithmes performants
Barres hautes = Algorithmes moins efficaces
```

##### **B. Distribution des makespans (Boxplot)**
- **Boîtes** : Quartiles (Q1, médiane, Q3)
- **Moustaches** : Min/Max ou 1.5*IQR
- **Points** : Valeurs aberrantes
- **Comparaison** : Variabilité entre algorithmes

**Interprétation** :
```
Boîte étroite = Algorithme stable
Boîte large = Algorithme variable
Médiane basse = Performance générale bonne
```

##### **C. Heatmap - Comparaison par instance**
- **Lignes** : Instances (échantillon de 15)
- **Colonnes** : Algorithmes
- **Couleurs** : Rouge (mauvais) → Vert (bon)
- **Valeurs** : Makespans exacts

**Interprétation** :
```
Colonnes vertes = Algorithmes souvent bons
Lignes contrastées = Instances discriminantes
Patterns = Comportements spécifiques
```

##### **D. Pourcentage de victoires (Secteurs)**
- **Secteurs** : Proportion d'instances où chaque algorithme est optimal
- **Couleurs** : Palette Set2 distincte
- **Pourcentages** : Affichés pour chaque secteur

**Interprétation** :
```
Gros secteurs = Algorithmes souvent optimaux
Petits secteurs = Algorithmes spécialisés
Absence = Algorithmes jamais optimaux
```

### **2. Tendances Makespans**

#### **📁 Fichier** : `resultats/graphiques/tendances_makespan.png`

**Graphique linéaire multi-séries** :
- **Axe X** : Index d'instance (ordre de traitement)
- **Axe Y** : Makespan (jours)
- **Lignes** : Une par algorithme
- **Marqueurs** : Points pour chaque instance

**Utilisation** :
- Identifier les instances difficiles (pics)
- Observer la constance des algorithmes
- Détecter les patterns temporels

### **3. Analyse Machine Learning**

#### **📁 Fichier** : `resultats/graphiques/analyse_ml.png`

**Contient 6 graphiques** :

##### **A. Taux de succès de l'IA (Secteurs)**
- **Vert** : Pourcentage de prédictions correctes
- **Rouge** : Pourcentage d'erreurs IA
- **Titre** : Taux global affiché

##### **B. Performance Recommandés vs Non-Recommandés (Boxplot)**
- **Boîte gauche** : Makespans des algorithmes recommandés par IA
- **Boîte droite** : Makespans des algorithmes non recommandés
- **Comparaison** : L'IA recommande-t-elle les meilleurs ?

##### **C. Fréquence des recommandations IA (Barres)**
- **Axe X** : Algorithmes
- **Axe Y** : Nombre de fois recommandé par l'IA
- **Valeurs** : Affichées sur barres

##### **D. Matrice de performance IA (Heatmap)**
- **Lignes** : Algorithmes optimaux réels
- **Colonnes** : Succès/Échec IA
- **Valeurs** : Nombre de cas
- **Couleurs** : Rouge (échec) → Vert (succès)

##### **E. Distribution des makespans par statut (Histogramme)**
- **Jaune** : Makespans optimaux
- **Bleu** : Makespans recommandés (non-optimaux)
- **Rouge** : Makespans autres algorithmes
- **Superposition** : Comparaison des distributions

##### **F. Amélioration apportée par l'IA (Histogramme)**
- **Axe X** : Pourcentage d'amélioration
- **Axe Y** : Nombre d'instances
- **Moyenne** : Affichée dans le titre

### **4. Comparaisons Multi-Projets**

#### **📁 Fichier** : `resultats/graphiques/comparaison_ml.png`

**Contient 4 graphiques** :

##### **A. Précision de l'IA par projet (Barres)**
- **Vert** : Projets avec IA correcte (100%)
- **Rouge** : Projets avec IA incorrecte (0%)
- **Ligne bleue** : Moyenne globale

##### **B. Comparaison Best vs Worst Makespans (Barres groupées)**
- **Jaune** : Meilleurs makespans
- **Rouge** : Pires makespans
- **Écart** : Potentiel d'amélioration

##### **C. Performance IA vs Optimal (Barres groupées)**
- **Jaune** : Makespans optimaux
- **Bleu** : Makespans moyens des recommandations IA

##### **D. Amélioration potentielle par projet (Barres)**
- **Vert** : Pourcentage d'amélioration possible
- **Valeurs** : Affichées sur barres

### **5. Analyses détaillées individuelles**

#### **📁 Fichiers** : `resultats/graphiques/detail_*.png`

**Contient 4 graphiques pour chaque projet** :

##### **A. Makespans par algorithme (Barres colorées)**
- **Couleurs** :
  - **Jaune** : Algorithme optimal
  - **Bleu** : Algorithmes recommandés par IA
  - **Rouge** : Autres algorithmes
- **Ligne rouge** : Seuil optimal

##### **B. Performance IA (Secteurs)**
- **Vert** : IA correcte
- **Rouge** : IA incorrecte
- **Pourcentage** : Affiché clairement

##### **C. Distribution recommandés/non-recommandés (Boxplot)**
- Comparaison statistique des performances

##### **D. Écarts par rapport à l'optimal (Barres)**
- **Axe Y** : Pourcentage d'écart
- **Ligne** : Seuil 0% (optimal)
- **Valeurs** : Pourcentages exacts

## 🛠️ Configuration des graphiques

### **Bibliothèques utilisées**
```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
```

### **Styles appliqués**
```python
# Style général
plt.style.use('default')
sns.set_palette("husl")

# Configuration matplotlib
plt.switch_backend('Agg')  # Mode non-interactif
```

### **Paramètres de qualité**
```python
# Sauvegarde haute résolution
plt.savefig(filename, 
           dpi=300,                # 300 DPI
           bbox_inches='tight',    # Ajustement automatique
           format='png')           # Format PNG
```

### **Palettes de couleurs**

#### **Algorithmes** :
```python
colors = sns.color_palette("viridis", n_algorithms)  # Viridis
colors = sns.color_palette("Set2", n_algorithms)     # Set2
colors = sns.color_palette("husl", n_algorithms)     # HUSL
```

#### **Status IA** :
```python
ia_colors = {
    'correct': '#28a745',    # Vert
    'incorrect': '#dc3545',  # Rouge
    'optimal': 'gold',       # Jaune
    'recommended': 'lightblue',  # Bleu clair
    'other': 'lightcoral'    # Rouge clair
}
```

## 📊 Interprétation des résultats

### **Métriques clés à surveiller**

#### **Performance IA** :
```
> 90% : Excellent
80-90% : Très bon
70-80% : Bon
< 70%  : À améliorer
```

#### **Amélioration moyenne** :
```
> 10% : Impact très significatif
5-10% : Impact significatif
1-5%  : Impact modéré
< 1%  : Impact faible
```

#### **Consistance des algorithmes** :
```
Faible variance : Algorithme stable
Forte variance : Algorithme sensible aux instances
```

### **Patterns typiques**

#### **IA performante** :
- Secteur vert dominant (>90%)
- Recommandations fréquentes des algorithmes optimaux
- Amélioration moyenne positive

#### **Projet équilibré** :
- Makespans similaires entre algorithmes
- Boxplots avec médianes proches
- Heatmap uniforme

#### **Projet discriminant** :
- Écarts importants entre algorithmes
- Heatmap contrastée
- IA sélective (peu de recommandations)

## 🔧 Personnalisation des graphiques

### **Modifier les couleurs**
```python
# Dans nettoyage_et_graphiques.py
custom_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
sns.set_palette(custom_colors)
```

### **Ajouter des graphiques**
```python
# Nouveau type de graphique
def create_custom_graph(data):
    plt.figure(figsize=(10, 6))
    
    # Votre code de visualisation
    plt.plot(data.x, data.y)
    plt.title('Mon Graphique Custom')
    
    # Sauvegarder
    plt.savefig('./resultats/graphiques/custom.png', dpi=300)
    plt.close()
```

### **Modifier les tailles**
```python
# Tailles de figures
large_figure = (15, 10)   # Graphiques principaux
medium_figure = (12, 8)   # Graphiques détaillés
small_figure = (8, 6)     # Graphiques simples
```

### **Personnaliser les titres**
```python
# Titres avec contexte
plt.title(f'Performance IA sur {len(instances)} instances\n'
         f'Période: {start_date} - {end_date}',
         fontsize=16, fontweight='bold')
```

## 📁 Organisation des fichiers graphiques

### **Structure générée**
```
resultats/graphiques/
├── analyse_makespan.png           # Analyse complète makespans
├── analyse_ml.png                 # Analyse complète ML
├── tendances_makespan.png         # Évolutions temporelles
├── comparaison_ml.png             # Comparaison multi-projets
├── detail_MSLIB_Set1_*.png        # Analyses individuelles
└── rapport_performance_ia.json    # Métriques JSON
```

### **Tailles typiques**
```
analyse_makespan.png     : ~500KB
analyse_ml.png          : ~450KB
tendances_makespan.png  : ~300KB
comparaison_ml.png      : ~400KB
detail_*.png           : ~250KB chacun
```

### **Métadonnées JSON**
```json
{
  "taux_succes_ia": 100.0,
  "instances_testees": 5,
  "amelioration_moyenne": 3.6,
  "algorithmes_les_plus_recommandes": {
    "EST": 5, "LPT": 4, "LST": 4, "SPT": 3
  },
  "algorithmes_les_plus_optimaux": {
    "LPT": 2, "LST": 2, "EST": 1
  }
}
```

## 🎯 Utilisation des graphiques

### **Présentations**
- **Format PNG haute résolution** pour slides
- **Titres explicites** pour compréhension rapide
- **Couleurs contrastées** pour projection

### **Rapports**
- **Métriques quantitatives** dans JSON
- **Visualisations complémentaires** pour insights
- **Comparaisons temporelles** pour suivi

### **Développement**
- **Graphiques de debug** pour validation
- **Analyses de convergence** pour optimisation
- **Distributions** pour compréhension des données

### **Publication**
- **Qualité publication** (300 DPI)
- **Formats vectoriels** disponibles sur demande
- **Légendes complètes** pour autonomie
