#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple simple d'utilisation du système ML pour MS-RCPSP
"""

import os
import json
import numpy as np
from binary_relevance_msrcpsp import (
    InstanceFeatureExtractor, 
    BinaryRelevanceClassifier, 
    MLIntegratedMSRCPSP
)


def exemple_simple():
    """Exemple d'utilisation basique du système ML"""
    print("=" * 60)
    print("EXEMPLE SIMPLE - SYSTÈME ML MS-RCPSP")
    print("=" * 60)
    
    # 1. Créer un extracteur de caractéristiques
    print("\n1. Initialisation de l'extracteur de caractéristiques...")
    extractor = InstanceFeatureExtractor()
    
    # 2. Données d'exemple d'une instance MS-RCPSP
    print("2. Création d'une instance d'exemple...")
    instance_exemple = {
        'nActs': 8,           # 8 activités
        'nRes': 3,            # 3 ressources
        'nSkills': 4,         # 4 compétences
        'dur': [2, 3, 1, 4, 2, 3, 1, 2],  # Durées des activités
        'sreq': [             # Compétences requises par activité
            [1, 0, 1, 0],     # Activité 0: compétences 0 et 2
            [0, 1, 1, 0],     # Activité 1: compétences 1 et 2
            [1, 1, 0, 0],     # Activité 2: compétences 0 et 1
            [0, 0, 1, 1],     # Activité 3: compétences 2 et 3
            [1, 0, 0, 1],     # Activité 4: compétences 0 et 3
            [0, 1, 0, 1],     # Activité 5: compétences 1 et 3
            [1, 1, 1, 0],     # Activité 6: compétences 0, 1 et 2
            [0, 0, 0, 1]      # Activité 7: compétence 3
        ],
        'mastery': [          # Compétences des ressources
            [1, 1, 0, 1],     # Ressource 0: compétences 0, 1 et 3
            [0, 1, 1, 1],     # Ressource 1: compétences 1, 2 et 3
            [1, 0, 1, 0]      # Ressource 2: compétences 0 et 2
        ],
        'precedence_graph': { # Graphe de précédence
            0: {'successors': [1, 2], 'predecessors': []},
            1: {'successors': [3], 'predecessors': [0]},
            2: {'successors': [4, 5], 'predecessors': [0]},
            3: {'successors': [6], 'predecessors': [1]},
            4: {'successors': [7], 'predecessors': [2]},
            5: {'successors': [7], 'predecessors': [2]},
            6: {'successors': [], 'predecessors': [3]},
            7: {'successors': [], 'predecessors': [4, 5]}
        },
        'est': [0, 2, 2, 5, 4, 4, 8, 7],      # Earliest Start Time
        'lst': [0, 3, 3, 6, 5, 5, 9, 8],      # Latest Start Time
        'lft': [2, 6, 4, 10, 7, 8, 10, 10],   # Latest Finish Time
        'float_dyn': [0, 1, 1, 1, 1, 1, 1, 1] # Flottement dynamique
    }
    
    # 3. Extraire les caractéristiques
    print("3. Extraction des caractéristiques...")
    features = extractor.extract_all_features(instance_exemple)
    
    print(f"   ✓ {len(features)} caractéristiques extraites")
    print("   Exemples de caractéristiques:")
    for i, (name, value) in enumerate(list(features.items())[:8]):
        print(f"     - {name}: {value:.3f}")
    
    # 4. Créer un classificateur (simulation d'entraînement)
    print("\n4. Simulation d'un modèle ML...")
    classifier = BinaryRelevanceClassifier()
    
    # Simuler des données d'entraînement
    np.random.seed(42)
    n_samples = 50
    n_features = len(features)
    algorithms = ['EST', 'LFT', 'MSLF', 'SPT', 'LPT', 'FCFS', 'LST']
    
    # Générer des features aléatoires
    X_train = np.random.randn(n_samples, n_features)
    
    # Générer des labels binaires (certains algorithmes bons pour certaines instances)
    y_train = np.zeros((n_samples, len(algorithms)))
    for i in range(n_samples):
        # Chaque instance a 2-4 "bons" algorithmes
        n_good = np.random.randint(2, 5)
        good_algos = np.random.choice(len(algorithms), n_good, replace=False)
        y_train[i, good_algos] = 1
    
    # Entraîner le modèle
    print("   ✓ Entraînement du modèle simulé...")
    try:
        classifier.fit(X_train, y_train, algorithms, list(features.keys()))
        print("   ✓ Modèle entraîné avec succès")
        
        # 5. Prédiction sur notre instance d'exemple
        print("\n5. Prédiction pour l'instance d'exemple...")
        X_test = np.array([list(features.values())]).reshape(1, -1)
        
        # Prédire les probabilités
        probabilities = classifier.predict_proba(X_test)
        best_rules = classifier.get_best_rules(X_test, top_k=3)
        
        print("   Algorithmes recommandés:")
        for i, algo in enumerate(best_rules[0]):
            prob = probabilities[algo][0]
            print(f"     {i+1}. {algo}: {prob:.3f} de probabilité")
        
        # 6. Analyse des caractéristiques importantes
        print("\n6. Caractéristiques les plus importantes:")
        try:
            feature_importance = classifier.get_feature_importance(top_n=5)
            for algo in best_rules[0][:2]:  # Pour les 2 meilleurs algorithmes
                if algo in feature_importance:
                    print(f"   Pour {algo}:")
                    for i, (feature, importance) in enumerate(list(feature_importance[algo].items())[:3], 1):
                        print(f"     {i}. {feature}: {importance:.4f}")
        except Exception as e:
            print(f"   Erreur dans l'analyse d'importance: {e}")
        
    except Exception as e:
        print(f"   ❌ Erreur d'entraînement: {e}")
    
    # 7. Interface complète (si disponible)
    print("\n7. Test de l'interface complète...")
    try:
        ml_system = MLIntegratedMSRCPSP()
        print("   ✓ Interface ML créée")
        print("   Note: Pour utiliser la résolution complète, un modèle")
        print("         pré-entraîné et le solveur MS-RCPSP sont nécessaires")
    except Exception as e:
        print(f"   ⚠️  Interface limitée: {e}")
    
    print("\n" + "=" * 60)
    print("EXEMPLE TERMINÉ")
    print("=" * 60)
    print("✅ Le système ML fonctionne correctement!")
    print("\nProchaines étapes:")
    print("1. Entraîner un modèle réel avec vos données:")
    print("   python binary_relevance_msrcpsp.py")
    print("2. Tester avec de vraies instances:")
    print("   python demo_ml_integration.py")


def exemple_features_avancees():
    """Démontre l'extraction avancée de caractéristiques"""
    print("\n" + "=" * 60)
    print("EXEMPLE AVANCÉ - EXTRACTION DE CARACTÉRISTIQUES")
    print("=" * 60)
    
    extractor = InstanceFeatureExtractor()
    
    # Instance plus complexe
    instance_complexe = {
        'nActs': 12,
        'nRes': 4,
        'nSkills': 6,
        'dur': [1, 2, 3, 2, 4, 1, 3, 2, 1, 3, 2, 1],
        'sreq': [
            [1, 0, 1, 0, 0, 1], [0, 1, 1, 1, 0, 0], [1, 1, 0, 0, 1, 0],
            [0, 0, 1, 1, 0, 1], [1, 0, 0, 1, 1, 0], [0, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1], [1, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 0, 0], [0, 0, 1, 0, 1, 1]
        ],
        'mastery': [
            [1, 1, 0, 1, 0, 1], [0, 1, 1, 1, 1, 0],
            [1, 0, 1, 0, 1, 1], [1, 1, 1, 0, 0, 1]
        ],
        'precedence_graph': {
            0: {'successors': [1, 2], 'predecessors': []},
            1: {'successors': [3, 4], 'predecessors': [0]},
            2: {'successors': [5], 'predecessors': [0]},
            3: {'successors': [6], 'predecessors': [1]},
            4: {'successors': [7, 8], 'predecessors': [1]},
            5: {'successors': [9], 'predecessors': [2]},
            6: {'successors': [10], 'predecessors': [3]},
            7: {'successors': [11], 'predecessors': [4]},
            8: {'successors': [11], 'predecessors': [4]},
            9: {'successors': [10], 'predecessors': [5]},
            10: {'successors': [], 'predecessors': [6, 9]},
            11: {'successors': [], 'predecessors': [7, 8]}
        },
        'est': [0, 1, 1, 3, 3, 4, 6, 5, 5, 7, 9, 8],
        'lst': [0, 2, 2, 4, 4, 5, 7, 6, 6, 8, 10, 9],
        'lft': [1, 4, 4, 6, 7, 6, 9, 8, 7, 10, 12, 10],
        'float_dyn': [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    
    # Extraire et analyser toutes les catégories de features
    print("1. Caractéristiques structurelles:")
    struct_features = extractor.extract_structural_features(instance_complexe)
    for name, value in list(struct_features.items())[:5]:
        print(f"   {name}: {value:.3f}")
    
    print("\n2. Caractéristiques du réseau:")
    network_features = extractor.extract_network_features(instance_complexe)
    for name, value in list(network_features.items())[:5]:
        print(f"   {name}: {value:.3f}")
    
    print("\n3. Caractéristiques des ressources:")
    resource_features = extractor.extract_resource_features(instance_complexe)
    for name, value in list(resource_features.items())[:5]:
        print(f"   {name}: {value:.3f}")
    
    print("\n4. Caractéristiques temporelles:")
    temporal_features = extractor.extract_temporal_features(instance_complexe)
    for name, value in list(temporal_features.items())[:5]:
        print(f"   {name}: {value:.3f}")
    
    # Analyse globale
    all_features = extractor.extract_all_features(instance_complexe)
    print(f"\n✓ Total: {len(all_features)} caractéristiques extraites")
    
    # Identifier les features les plus distinctives
    print("\n5. Analyse de la complexité de l'instance:")
    complexity_score = 0
    if all_features['network_density'] > 0.3:
        complexity_score += 1
        print("   • Réseau dense détecté")
    if all_features['resource_flexibility'] > 2.0:
        complexity_score += 1
        print("   • Ressources très flexibles")
    if all_features['duration_cv'] > 0.5:
        complexity_score += 1
        print("   • Durées très variables")
    if all_features['critical_activities_ratio'] > 0.7:
        complexity_score += 1
        print("   • Beaucoup d'activités critiques")
    
    print(f"\n   Score de complexité: {complexity_score}/4")
    
    if complexity_score >= 3:
        print("   → Instance complexe: algorithmes avancés recommandés")
    elif complexity_score >= 2:
        print("   → Instance moyenne: mix d'algorithmes approprié")
    else:
        print("   → Instance simple: algorithmes de base suffisants")


def main():
    """Menu principal des exemples"""
    print("EXEMPLES D'UTILISATION - SYSTÈME ML MS-RCPSP")
    print("=" * 60)
    
    print("\nExemples disponibles:")
    print("1. Exemple simple et complet")
    print("2. Extraction avancée de caractéristiques")
    print("3. Les deux exemples")
    
    try:
        choice = input("\nChoisissez un exemple (1-3, ou Entrée pour tout): ").strip()
        
        if choice == "1":
            exemple_simple()
        elif choice == "2":
            exemple_features_avancees()
        else:
            exemple_simple()
            exemple_features_avancees()
            
        print("\n🎉 Exemples terminés avec succès!")
        print("\nPour aller plus loin:")
        print("• Entraînez un vrai modèle: python binary_relevance_msrcpsp.py")
        print("• Tests interactifs: python demo_ml_integration.py")
        print("• Documentation: README_ML.md")
        
    except KeyboardInterrupt:
        print("\nExemples interrompus.")
    except Exception as e:
        print(f"\nErreur dans les exemples: {e}")


if __name__ == "__main__":
    main()
