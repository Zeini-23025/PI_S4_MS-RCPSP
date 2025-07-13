#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant de démarrage pour le système ML MS-RCPSP
"""

import os
import sys


def check_requirements():
    """Vérifie les prérequis du système"""
    print("🔍 Vérification des prérequis...")
    
    # Vérifier Python
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ requis")
        return False
    else:
        print(f"✅ Python {sys.version.split()[0]}")
    
    # Vérifier les modules
    required_modules = ['numpy', 'pandas', 'sklearn']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} manquant")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n💡 Pour installer les modules manquants:")
        print(f"   pip install {' '.join(missing_modules)}")
        return False
    
    # Vérifier les fichiers
    required_files = [
        'binary_relevance_msrcpsp.py',
        'exemple_ml.py',
        'demo_ml_integration.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n💡 Fichiers manquants: {missing_files}")
        return False
    
    return True


def show_menu():
    """Affiche le menu principal"""
    print("\n" + "="*60)
    print("🤖 ASSISTANT ML MS-RCPSP")
    print("="*60)
    print()
    print("Que voulez-vous faire ?")
    print()
    print("1. 🧪 Tester le système (exemples simples)")
    print("2. 🎓 Entraîner un nouveau modèle ML")
    print("3. 🚀 Utiliser le modèle ML pour résoudre")
    print("4. 🎮 Interface interactive et démonstrations")
    print("5. 📚 Afficher la documentation")
    print("6. 🔧 Vérifier l'installation")
    print("7. ❌ Quitter")
    print()


def run_command(cmd, description):
    """Exécute une commande avec description"""
    print(f"\n🚀 {description}...")
    print(f"Commande: {cmd}")
    print("-" * 50)
    
    try:
        os.system(cmd)
    except KeyboardInterrupt:
        print("\nInterruption utilisateur.")
    except Exception as e:
        print(f"Erreur: {e}")


def show_documentation():
    """Affiche la documentation disponible"""
    print("\n📚 DOCUMENTATION DISPONIBLE")
    print("="*50)
    
    docs = [
        ("README_ML.md", "Documentation technique complète"),
        ("GUIDE_ML.md", "Guide utilisateur simplifié"),
        ("binary_relevance_msrcpsp.py", "Code source principal (avec docstrings)"),
        ("exemple_ml.py", "Exemples commentés d'utilisation")
    ]
    
    for file, description in docs:
        if os.path.exists(file):
            print(f"✅ {file:<25} - {description}")
        else:
            print(f"❌ {file:<25} - {description} (manquant)")
    
    print()
    print("💡 Conseils:")
    print("   • Commencez par GUIDE_ML.md pour une vue d'ensemble")
    print("   • Consultez README_ML.md pour les détails techniques")
    print("   • Exécutez exemple_ml.py pour voir le code en action")


def main():
    """Fonction principale"""
    print("🤖 Assistant de démarrage ML MS-RCPSP")
    print("="*50)
    
    # Vérification initiale
    if not check_requirements():
        print("\n❌ Prérequis non satisfaits. Veuillez corriger les problèmes ci-dessus.")
        return
    
    print("\n✅ Tous les prérequis sont satisfaits!")
    
    while True:
        show_menu()
        
        try:
            choice = input("Votre choix (1-7): ").strip()
            
            if choice == "1":
                run_command("python3 exemple_ml.py", "Test avec exemples simples")
            
            elif choice == "2":
                print("\n📋 Notes importantes pour l'entraînement:")
                print("   • Assurez-vous d'avoir des instances dans ./Instances/")
                print("   • Le processus peut prendre plusieurs minutes")
                print("   • Le modèle sera sauvé dans ./resultats/")
                input("\nAppuyez sur Entrée pour continuer...")
                run_command("python3 binary_relevance_msrcpsp.py", "Entraînement du modèle ML")
            
            elif choice == "3":
                model_path = "./resultats/binary_relevance_model.pkl"
                if not os.path.exists(model_path):
                    print(f"\n❌ Modèle non trouvé: {model_path}")
                    print("💡 Entraînez d'abord un modèle (option 2)")
                else:
                    run_command("python3 binary_relevance_msrcpsp.py", "Utilisation du modèle ML")
            
            elif choice == "4":
                run_command("python3 demo_ml_integration.py", "Interface interactive")
            
            elif choice == "5":
                show_documentation()
            
            elif choice == "6":
                if check_requirements():
                    print("\n✅ Installation OK!")
                else:
                    print("\n❌ Problèmes détectés")
            
            elif choice == "7":
                print("\n👋 Au revoir!")
                break
            
            else:
                print("\n❌ Choix invalide. Veuillez entrer un numéro entre 1 et 7.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"\n❌ Erreur: {e}")


if __name__ == "__main__":
    main()
