# 🔧 Installation et Configuration

## 📋 Prérequis système

### **Système d'exploitation**
- ✅ **Linux** (Ubuntu, Debian, CentOS, etc.)
- ✅ **macOS** (10.14+)
- ✅ **Windows** (10/11)

### **Python**
- **Version requise** : Python 3.8+
- **Version recommandée** : Python 3.10+
- **Version testée** : Python 3.13

### **Vérification Python**
```bash
python3 --version
# Sortie attendue : Python 3.8+ 

which python3
# Vérifier que Python est dans le PATH
```

## 📦 Installation automatique (Recommandée)

### **Méthode 1 : Installation complète automatique**
```bash
# Cloner ou télécharger le projet
cd MS-RCPSP/

# Lancement automatique avec installation des dépendances
python3 run_project.py
```

**Ce qui se passe** :
1. ✅ Vérification automatique des dépendances
2. ✅ Installation automatique des packages manquants
3. ✅ Configuration complète du système
4. ✅ Tests de validation

**Sortie attendue** :
```
📦 INSTALLATION DES DÉPENDANCES
========================================
✅ numpy
❌ scikit-learn manquant
✅ matplotlib
✅ pandas
✅ seaborn

📦 Installation des packages manquants...
✅ scikit-learn installé
✅ Toutes les dépendances sont disponibles
```

## 🛠️ Installation manuelle

### **Étape 1 : Dépendances Python**
```bash
# Installation avec pip
pip install numpy scikit-learn matplotlib pandas seaborn

# OU avec conda
conda install numpy scikit-learn matplotlib pandas seaborn

# OU avec requirements.txt (si fourni)
pip install -r requirements.txt
```

### **Étape 2 : Vérification des dépendances**
```python
# Test d'importation
python3 -c "
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
print('✅ Toutes les dépendances sont installées')
"
```

### **Étape 3 : Test du système**
```bash
# Test minimal
python3 -c "
from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
print('✅ Modules MS-RCPSP fonctionnels')
"
```

## 📋 Détail des dépendances

### **Dépendances obligatoires**

#### **NumPy** (Calculs numériques)
```bash
pip install numpy>=1.21.0
```
**Usage** : Calculs matriciels, caractéristiques numériques

#### **Scikit-learn** (Machine Learning)
```bash
pip install scikit-learn>=1.0.0
```
**Usage** : Modèles ML, validation croisée, métriques

#### **Matplotlib** (Visualisations de base)
```bash
pip install matplotlib>=3.5.0
```
**Usage** : Graphiques, plots, sauvegarde PNG

#### **Pandas** (Manipulation de données)
```bash
pip install pandas>=1.3.0
```
**Usage** : DataFrames, analyses statistiques, export CSV

#### **Seaborn** (Visualisations avancées)
```bash
pip install seaborn>=0.11.0
```
**Usage** : Heatmaps, boxplots, palettes de couleurs

### **Dépendances optionnelles**

#### **Joblib** (Sérialisation modèles)
```bash
pip install joblib>=1.0.0
```
**Usage** : Sauvegarde/chargement des modèles ML
**Note** : Inclus avec scikit-learn

#### **Pathlib** (Gestion des chemins)
**Usage** : Manipulation des fichiers et dossiers
**Note** : Inclus dans Python 3.4+

## 🏗️ Structure de l'environnement

### **Environnement virtuel (Recommandé)**
```bash
# Créer un environnement virtuel
python3 -m venv ms_rcpsp_env

# Activer l'environnement
# Linux/macOS :
source ms_rcpsp_env/bin/activate
# Windows :
ms_rcpsp_env\Scripts\activate

# Installer les dépendances
pip install numpy scikit-learn matplotlib pandas seaborn

# Désactiver l'environnement (quand terminé)
deactivate
```

### **Conda (Alternative)**
```bash
# Créer un environnement conda
conda create -n ms_rcpsp python=3.10

# Activer l'environnement
conda activate ms_rcpsp

# Installer les dépendances
conda install numpy scikit-learn matplotlib pandas seaborn

# Désactiver l'environnement
conda deactivate
```

## 📁 Configuration des dossiers

### **Structure requise**
```
MS-RCPSP/
├── *.py                    # Scripts Python
├── Instances/              # Instances de test (.msrcp)
├── resultats/              # Résultats et modèles (créé auto)
├── resultats_ml/           # Résultats ML (créé auto)
├── docs/                   # Documentation
└── README.md              # Ce fichier
```

### **Permissions requises**
```bash
# Donner les permissions d'exécution
chmod +x *.py
chmod +x run_project.py

# Vérifier les permissions d'écriture
ls -la
# Doit afficher rwx pour le propriétaire
```

### **Création automatique des dossiers**
Les dossiers de sortie sont créés automatiquement :
```python
# Dans le code
os.makedirs("./resultats", exist_ok=True)
os.makedirs("./resultats_ml", exist_ok=True) 
os.makedirs("./resultats/graphiques", exist_ok=True)
```

## 🧪 Validation de l'installation

### **Test complet automatique**
```bash
# Test d'installation et de fonctionnement
python3 run_project.py
```

**Résultats attendus** :
- ✅ Toutes les dépendances détectées
- ✅ Modèle ML entraîné (930KB)
- ✅ Résultats ML générés (5 fichiers JSON)
- ✅ Graphiques créés (4+ images PNG)
- ✅ Taux de succès IA : 100%

### **Tests individuels**

#### **Test 1 : Génération de données**
```bash
python3 makespan_calculator.py
```
**Attendu** : Fichiers JSON dans `resultats/makespan_details/`

#### **Test 2 : Entraînement ML**
```bash
python3 binary_relevance_msrcpsp.py
# Choisir option 1
```
**Attendu** : Fichier `resultats/binary_relevance_model.pkl`

#### **Test 3 : Interface utilisateur**
```bash
python3 assistant_ml.py
```
**Attendu** : Menu interactif fonctionnel

#### **Test 4 : Visualisations**
```bash
python3 nettoyage_et_graphiques.py
# Choisir option 4
```
**Attendu** : Images PNG dans `resultats/graphiques/`

## 🔧 Configuration avancée

### **Variables d'environnement**
```bash
# Optimisation Python
export PYTHONHASHSEED=0          # Reproductibilité
export PYTHONUNBUFFERED=1        # Sortie temps réel

# Matplotlib backend (pour serveurs sans écran)
export MPLBACKEND=Agg

# Threads scikit-learn
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
```

### **Configuration matplotlib**
```python
# Dans le code, pour serveurs
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif

import matplotlib.pyplot as plt
plt.switch_backend('Agg')
```

### **Réglages de performance**
```python
# Parallélisation scikit-learn
from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(
    n_jobs=-1,              # Utiliser tous les cœurs
    random_state=42         # Reproductibilité
)
```

### **Gestion mémoire**
```python
# Pour traitement de gros volumes
import gc

# Forcer le garbage collection
gc.collect()

# Limiter la mémoire matplotlib
import matplotlib
matplotlib.rcParams['figure.max_open_warning'] = 0
```

## 🚨 Résolution de problèmes

### **Problème 1 : ImportError modules**
```
Erreur : ModuleNotFoundError: No module named 'sklearn'
```
**Solutions** :
```bash
# Vérifier pip
which pip3
pip3 --version

# Installer manuellement
pip3 install scikit-learn

# Vérifier l'environnement Python
python3 -c "import sys; print(sys.path)"
```

### **Problème 2 : Permissions refusées**
```
Erreur : PermissionError: [Errno 13] Permission denied
```
**Solutions** :
```bash
# Changer les permissions
chmod +x *.py
chmod 755 ./

# Changer le propriétaire (si nécessaire)
sudo chown -R $USER:$USER ./

# Vérifier l'espace disque
df -h
```

### **Problème 3 : Matplotlib display**
```
Erreur : no display name and no $DISPLAY environment variable
```
**Solutions** :
```bash
# Définir le backend non-interactif
export MPLBACKEND=Agg

# OU dans le code Python
import matplotlib
matplotlib.use('Agg')
```

### **Problème 4 : Version Python incompatible**
```
Erreur : SyntaxError: f-strings incompatibles
```
**Solutions** :
```bash
# Vérifier la version
python3 --version

# Installer Python plus récent
sudo apt update
sudo apt install python3.10

# Utiliser pyenv pour gestion des versions
curl https://pyenv.run | bash
pyenv install 3.10.0
pyenv global 3.10.0
```

### **Problème 5 : Espace disque insuffisant**
```
Erreur : No space left on device
```
**Solutions** :
```bash
# Vérifier l'espace
df -h

# Nettoyer le cache pip
pip3 cache purge

# Nettoyer les fichiers temporaires
rm -rf /tmp/pip*
rm -rf ~/.cache/pip
```

## 📊 Vérification post-installation

### **Checklist de validation**
```bash
# ✅ Python 3.8+
python3 --version

# ✅ Dépendances installées
python3 -c "import numpy, sklearn, matplotlib, pandas, seaborn; print('OK')"

# ✅ Dossiers créés
ls -la resultats/ resultats_ml/

# ✅ Modèle ML fonctionnel
ls -lh resultats/binary_relevance_model.pkl

# ✅ Résultats générés
ls resultats_ml/*.json

# ✅ Graphiques créés
ls resultats/graphiques/*.png
```

### **Métriques de performance**
```
Temps d'installation   : < 5 minutes
Temps de premier test  : < 60 secondes
Espace disque requis   : < 100 MB
Mémoire RAM minimum    : 512 MB
Processeur minimum     : 1 cœur (recommandé : 4+ cœurs)
```

### **Test de charge**
```bash
# Test sur toutes les instances disponibles
# (seulement si >1GB d'espace disque)
python3 binary_relevance_msrcpsp.py
# Choisir option 4 (traitement en lot)
```

## 🎯 Configuration pour production

### **Optimisations recommandées**
```python
# Dans binary_relevance_msrcpsp.py
MAX_INSTANCES = 100        # Au lieu de 20
TOLERANCE = 0.05          # Au lieu de 0.1
N_ESTIMATORS = 200        # Au lieu de 100

# Parallélisation
N_JOBS = -1               # Utiliser tous les cœurs
```

### **Monitoring et logs**
```python
import logging

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ms_rcpsp.log'),
        logging.StreamHandler()
    ]
)
```

### **Sauvegarde automatique**
```bash
# Script de sauvegarde
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_${DATE}.tar.gz resultats/ resultats_ml/ docs/
```

### **Déploiement serveur**
```bash
# Service systemd (exemple)
sudo tee /etc/systemd/system/ms-rcpsp.service > /dev/null <<EOF
[Unit]
Description=MS-RCPSP Service
After=network.target

[Service]
Type=simple
User=msrcpsp
WorkingDirectory=/opt/ms-rcpsp/
ExecStart=/usr/bin/python3 run_project.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable ms-rcpsp
sudo systemctl start ms-rcpsp
```
