#!/bin/bash

# =============================================================================
# PROJET MS-RCPSP AVEC MACHINE LEARNING - FLUX DE TRAVAIL AUTOMATISÉ
# =============================================================================
# Ce script exécute le flux de travail complet du projet :
# 1. Génération des données de performance (makespan)
# 2. Entraînement du modèle Machine Learning
# 3. Démonstration de résolution guidée par IA
#
# Prérequis : Python 3.7+, numpy, pandas, scikit-learn
# Durée estimée : 10-60 minutes selon le nombre d'instances
# =============================================================================

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage coloré
print_section() {
    echo -e "\n${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifications préalables
print_section "VÉRIFICATIONS PRÉALABLES"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 non trouvé. Veuillez installer Python 3.7+"
    exit 1
fi
print_success "Python 3 trouvé : $(python3 --version)"

# Vérifier les modules Python
python3 -c "import numpy, pandas, sklearn" 2>/dev/null && {
    print_success "Modules ML disponibles (numpy, pandas, sklearn)"
} || {
    print_error "Modules manquants. Installer avec: pip install numpy pandas scikit-learn"
    exit 1
}

# Vérifier les fichiers requis
for file in "msrcpsp_final.py" "binary_relevance_msrcpsp.py"; do
    if [[ -f "$file" ]]; then
        print_success "Fichier trouvé : $file"
    else
        print_error "Fichier manquant : $file"
        exit 1
    fi
done

# Vérifier les instances
if [[ -d "Instances" ]]; then
    instance_count=$(find Instances/ -name "*.msrcp" -o -name "*.dzn" 2>/dev/null | wc -l)
    if [[ $instance_count -gt 0 ]]; then
        print_success "Instances trouvées : $instance_count fichiers"
    else
        print_warning "Aucune instance trouvée dans Instances/"
        print_warning "Le script utilisera des données simulées pour l'entraînement ML"
    fi
else
    print_warning "Dossier Instances/ non trouvé"
    mkdir -p Instances
fi

# Créer les dossiers de résultats
mkdir -p resultats resultats_ml

print_section "DÉMARRAGE DU FLUX DE TRAVAIL"

# Étape 1: Générer les données de performance (Makespan)
print_section "ÉTAPE 1: GÉNÉRATION DES DONNÉES DE PERFORMANCE"
echo "Cette étape exécute tous les algorithmes sur les instances disponibles"
echo "et sauvegarde les résultats de makespan pour l'entraînement ML."
echo "Durée estimée : 5-30 minutes selon le nombre d'instances"
echo ""

# Optionnel : demander confirmation si beaucoup d'instances
if [[ $instance_count -gt 100 ]]; then
    print_warning "Attention : $instance_count instances détectées"
    print_warning "L'exécution peut prendre du temps (>20 minutes)"
    read -p "Continuer ? (o/N) : " -r
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        print_warning "Arrêt demandé par l'utilisateur"
        exit 0
    fi
fi

echo "Lancement de la génération des données..."
if python3 msrcpsp_final.py; then
    print_success "Données de performance générées avec succès"
    
    # Vérifier les résultats
    if [[ -d "resultats/makespan_details" ]]; then
        makespan_files=$(find resultats/makespan_details/ -name "*_makespans.json" 2>/dev/null | wc -l)
        print_success "Fichiers de makespan créés : $makespan_files"
    fi
else
    print_error "Échec de la génération des données"
    print_warning "Le script va continuer avec la simulation ML..."
fi

# Étape 2: Entraîner le Modèle de Machine Learning
print_section "ÉTAPE 2: ENTRAÎNEMENT DU MODÈLE MACHINE LEARNING"
echo "Cette étape analyse les données de makespan, extrait 43 caractéristiques"
echo "et entraîne le modèle Binary Relevance pour prédire les meilleurs algorithmes."
echo "Durée estimée : 2-10 minutes selon le dataset"
echo ""

echo "Lancement de l'entraînement ML..."
if python3 -c "from binary_relevance_msrcpsp import train_new_model; train_new_model()"; then
    print_success "Modèle ML entraîné avec succès"
    
    # Vérifier le modèle créé
    if [[ -f "resultats/binary_relevance_model.pkl" ]]; then
        model_size=$(du -h resultats/binary_relevance_model.pkl | cut -f1)
        print_success "Modèle sauvegardé : $model_size"
    fi
    
    if [[ -f "resultats/binary_relevance_metadata.json" ]]; then
        print_success "Métadonnées du modèle créées"
    fi
else
    print_error "Échec de l'entraînement ML"
    print_warning "Vérifiez les données de makespan ou utilisez exemple_ml.py"
    exit 1
fi

# Étape 3: Utiliser le Modèle pour Résoudre une Instance
print_section "ÉTAPE 3: DÉMONSTRATION DE RÉSOLUTION GUIDÉE PAR IA"
echo "Cette étape utilise le modèle ML entraîné pour prédire les meilleurs"
echo "algorithmes et résoudre une instance spécifique de manière optimisée."
echo "Durée estimée : <30 secondes"
echo ""

# Trouver une instance de test
test_instance=""
if [[ -f "Instances/MSLIB_Set1_1.msrcp" ]]; then
    test_instance="Instances/MSLIB_Set1_1.msrcp"
elif [[ -f "Instances/MSLIB_Set1_10.msrcp" ]]; then
    test_instance="Instances/MSLIB_Set1_10.msrcp"
else
    # Prendre la première instance disponible
    test_instance=$(find Instances/ -name "*.msrcp" -o -name "*.dzn" 2>/dev/null | head -1)
fi

if [[ -n "$test_instance" ]]; then
    echo "Instance de test : $test_instance"
    echo "Lancement de la résolution guidée par IA..."
    
    if python3 -c "
from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
import json

try:
    ml_system = MLIntegratedMSRCPSP('./resultats/binary_relevance_model.pkl')
    result = ml_system.solve_with_ml_guidance('$test_instance')
    
    if result:
        print('\\n📊 RÉSULTATS DE LA RÉSOLUTION GUIDÉE PAR IA :')
        print('=' * 60)
        print(f'Instance : {result.get(\"instance\", \"$test_instance\")}')
        print(f'Algorithmes recommandés : {result.get(\"recommended_algorithms\", [])}')
        print(f'Meilleur algorithme : {result.get(\"best_algorithm\", \"N/A\")}')
        print(f'Meilleur makespan : {result.get(\"best_makespan\", \"N/A\")}')
        
        if 'all_results' in result:
            print('\\nDétail des résultats :')
            for algo, makespan in result['all_results'].items():
                marker = '🏆' if algo == result.get('best_algorithm') else '  '
                print(f'  {marker} {algo}: {makespan}')
        
        if 'improvement' in result:
            print(f'\\nAmélioration : {result[\"improvement\"]}')
        
        print('=' * 60)
    else:
        print('❌ Aucun résultat obtenu')
        
except Exception as e:
    print(f'❌ Erreur lors de la résolution : {e}')
    exit(1)
"; then
        print_success "Résolution guidée par IA réussie"
    else
        print_error "Échec de la résolution guidée"
        exit 1
    fi
else
    print_warning "Aucune instance de test trouvée"
    print_warning "Créez le dossier Instances/ avec des fichiers .msrcp"
fi

print_section "FLUX DE TRAVAIL TERMINÉ AVEC SUCCÈS!"
echo ""
echo "🎉 Votre système MS-RCPSP avec Machine Learning est opérationnel !"
echo ""
echo "Fichiers créés :"
echo "  📁 resultats/binary_relevance_model.pkl    (Modèle ML entraîné)"
echo "  📁 resultats/binary_relevance_metadata.json (Métadonnées du modèle)"
echo "  📁 resultats/makespan_details/              (Données d'entraînement)"
echo ""
echo "Prochaines étapes recommandées :"
echo "  🚀 python3 assistant_ml.py                 (Interface guidée)"
echo "  🧪 python3 test_automatique.py             (Tests automatisés)"
echo "  📊 python3 demo_ml_integration.py          (Démonstrations)"
echo "  📚 Consulter README_ML.md                  (Documentation technique)"
echo ""
print_success "Mission accomplie ! 🎯"

