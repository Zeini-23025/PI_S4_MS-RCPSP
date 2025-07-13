#!/usr/bin/env python3
"""
MSRCPSP Demo - Démonstration complète du solver
"""

import os
import sys


def print_header():
    """Affiche l'en-tête du programme"""
    print("=" * 60)
    print("🚀 MSRCPSP SOLVER - Demonstration Complète")
    print("   Multi-Skilled Resource-Constrained Project Scheduling")
    print("=" * 60)
    print()


def print_problem_description():
    """Explique le problème MSRCPSP"""
    print("🎯 QU'EST-CE QUE LE MSRCPSP ?")
    print("-" * 30)
    print("Le MSRCPSP est un problème d'ordonnancement de projet où :")
    print("• 👥 Les ressources ont plusieurs compétences à différents niveaux")
    print("• 🔗 Les activités ont des dépendances entre elles")
    print("• 🎯 L'objectif est de minimiser la durée totale (makespan)")
    print("• ⚠️  Contraintes: précédence, ressources limitées, compétences requises")
    print()


def print_algorithms_explanation():
    """Explique les algorithmes implémentés"""
    print("🧠 ALGORITHMES DE PRIORITÉ IMPLÉMENTÉS")
    print("-" * 40)
    print("• EST  - Earliest Start Time        : Commence dès que possible")
    print("• LFT  - Latest Finish Time         : Priorise par échéance")
    print("• MSLF - Minimum Slack Time         : Priorise les activités critiques")
    print("• SPT  - Shortest Processing Time   : Fait les tâches courtes d'abord")
    print("• LPT  - Longest Processing Time    : Fait les tâches longues d'abord")
    print("• FCFS - First Come First Served    : Ordre d'arrivée simple")
    print("• LST  - Latest Start Time          : Utilise la flexibilité temporelle")
    print()
    print("💡 NOTE IMPORTANTE:")
    print("Les algorithmes donnent souvent les MÊMES résultats car :")
    print("• 🔒 Contraintes fortes (ressources + compétences)")
    print("• 🛤️  Chemin critique dominant")
    print("• 📊 Instances relativement simples")
    print("• ⚠️  Limite d'itérations atteinte (blocages)")
    print()
    print("Pour voir plus de différences :")
    print("• Utilisez des instances plus complexes")
    print("• Testez sur des projets avec plus d'activités")
    print("• Analysez le temps d'exécution et la stabilité")
    print()


def print_instance_format():
    """Explique le format des instances"""
    print("📁 FORMAT DES INSTANCES (.msrcp)")
    print("-" * 33)
    print("Chaque fichier .msrcp contient :")
    print("• 🧩 Module Projet      : Activités, durées, dépendances")
    print("• 👷 Module Ressources  : Compétences binaires + niveaux")
    print("• 🎯 Module Exigences   : Compétences requises par activité")
    print("• 📈 Modules Coûts      : Coûts fixes/variables (optionnel)")
    print()
    print("Exemple d'activité :")
    print("  7  3  11 15 23")
    print("  ↑  ↑  ↑")
    print("  │  │  └─ Successeurs (activités 11, 15, 23)")
    print("  │  └─ Nombre de successeurs")
    print("  └─ Durée de l'activité")
    print()


def print_results_format():
    """Explique le format des résultats"""
    print("📊 FORMAT DES RÉSULTATS")
    print("-" * 25)
    print("Le solver génère :")
    print("• 📈 makespan_comparison.csv : Comparaison des algorithmes")
    print("• 📝 detailed_results.json  : Résultats détaillés par instance")
    print("• 📁 resultats/<ALG>/        : Résultats par algorithme")
    print()
    print("Structure d'un résultat :")
    print("{")
    print('  "makespan": 35,')
    print('  "schedule": [')
    print('    [activity_id, start_time, end_time, [resources]],')
    print('    [1, 0, 7, [0, 1]],  # Activité 1: temps 0-7, ressources 0,1')
    print('    [2, 7, 8, [2]]      # Activité 2: temps 7-8, ressource 2')
    print('  ]')
    print('}')
    print()


def run_demo():
    """Lance la démonstration"""
    print("🔬 DÉMONSTRATION EN COURS...")
    print("-" * 28)
    
    # Vérifier si le solver final existe
    if not os.path.exists("msrcpsp_final.py"):
        print("❌ Fichier msrcpsp_final.py non trouvé!")
        return
    
    # Vérifier s'il y a des instances
    if not os.path.exists("Instances") or not os.listdir("Instances"):
        print("⚠️  Aucune instance trouvée dans le répertoire 'Instances/'")
        print("💡 Veuillez placer vos fichiers .msrcp dans ce répertoire")
        return
    
    instances = [f for f in os.listdir("Instances") if f.endswith('.msrcp')]
    print(f"✅ {len(instances)} instances trouvées")
    
    # Lancer le solver
    print("\n🚀 Exécution du solver...")
    print("⏳ Veuillez patienter...")
    print()
    
    os.system("python3 msrcpsp_final.py")
    
    # Vérifier les résultats
    if os.path.exists("resultats/test_comparison.csv"):
        print("\n✅ RÉSULTATS GÉNÉRÉS AVEC SUCCÈS!")
        print("📁 Vérifiez le répertoire 'resultats/' pour les détails")
        
        # Afficher un extrait du CSV
        try:
            with open("resultats/test_comparison.csv", 'r') as f:
                lines = f.readlines()
                print("\n📊 Aperçu des résultats (test_comparison.csv):")
                print("-" * 50)
                for line in lines[:6]:  # Premières lignes
                    print(f"   {line.strip()}")
                if len(lines) > 6:
                    print("   ...")
        except Exception as e:
            print(f"⚠️  Impossible de lire les résultats: {e}")
    else:
        print("\n⚠️  Aucun résultat généré")


def print_usage_instructions():
    """Instructions d'utilisation"""
    print("💡 COMMENT UTILISER LE SOLVER")
    print("-" * 31)
    print("1️⃣  Placez vos fichiers .msrcp dans le répertoire 'Instances/'")
    print("2️⃣  Exécutez : python3 msrcpsp_final.py")
    print("3️⃣  Consultez les résultats dans 'resultats/'")
    print()
    print("🔧 FICHIERS PRINCIPAUX :")
    print("• msrcpsp_final.py  : Solver principal")
    print("• instances.md      : Documentation format .msrcp")
    print("• per.md           : Documentation algorithmes")
    print("• problem.md       : Description du problème")
    print("• README.md        : Guide complet")
    print()


def print_footer():
    """Pied de page"""
    print("🎓 RÉFÉRENCE ACADÉMIQUE")
    print("-" * 22)
    print("Basé sur les spécifications du projet de recherche :")
    print('"Project Management with Dynamic Scheduling"')
    print("Plus d'infos : projectmanagement.ugent.be/research/data")
    print()
    print("=" * 60)
    print("🏁 Fin de la démonstration")
    print("   Merci d'avoir utilisé MSRCPSP Solver!")
    print("=" * 60)


def main():
    """Fonction principale de démonstration"""
    print_header()
    
    # Menu interactif
    while True:
        print("🔍 QUE VOULEZ-VOUS VOIR ?")
        print("1️⃣  Description du problème MSRCPSP")
        print("2️⃣  Algorithmes de priorité")
        print("3️⃣  Format des instances")
        print("4️⃣  Format des résultats")
        print("5️⃣  Lancer la démonstration")
        print("6️⃣  Instructions d'utilisation")
        print("0️⃣  Quitter")
        print()
        
        try:
            choice = input("Votre choix (0-6) : ").strip()
            print()
            
            if choice == "1":
                print_problem_description()
            elif choice == "2":
                print_algorithms_explanation()
            elif choice == "3":
                print_instance_format()
            elif choice == "4":
                print_results_format()
            elif choice == "5":
                run_demo()
                break
            elif choice == "6":
                print_usage_instructions()
            elif choice == "0":
                print("👋 Au revoir!")
                break
            else:
                print("❌ Choix invalide, veuillez réessayer")
            
            input("\nAppuyez sur Entrée pour continuer...")
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    print_footer()


if __name__ == "__main__":
    main()
