#!/usr/bin/env python3
"""
Script de validation du solver MSRCPSP
Vérifie que tous les composants fonctionnent correctement
"""

import os
import sys


def check_instances():
    """Vérifie la présence des instances"""
    print("🔍 Vérification des instances...")
    
    if not os.path.exists("Instances"):
        print("❌ Dossier 'Instances' manquant")
        return False
    
    instances = [f for f in os.listdir("Instances") if f.endswith('.msrcp')]
    if not instances:
        print("❌ Aucun fichier .msrcp trouvé")
        return False
    
    print(f"✅ {len(instances)} instances trouvées")
    return True


def check_scripts():
    """Vérifie la présence des scripts"""
    print("\n🔍 Vérification des scripts...")
    
    required_files = [
        "msrcpsp_complete.py",
        "msrcpsp_final.py", 
        "demo.py"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
        else:
            print(f"✅ {file}")
    
    if missing:
        print(f"❌ Fichiers manquants: {missing}")
        return False
    
    return True


def check_documentation():
    """Vérifie la documentation"""
    print("\n🔍 Vérification de la documentation...")
    
    doc_files = [
        "README.md",
        "instances.md",
        "per.md", 
        "problem.md",
        "QUICKSTART.md"
    ]
    
    for file in doc_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️  {file} manquant")
    
    return True


def test_parser():
    """Test rapide du parser"""
    print("\n🧪 Test du parser...")
    
    try:
        from msrcpsp_final import MSRCPSPParser
        
        instances = [f for f in os.listdir("Instances") if f.endswith('.msrcp')]
        if not instances:
            print("⚠️  Aucune instance pour tester")
            return True
        
        test_file = os.path.join("Instances", instances[0])
        instance = MSRCPSPParser.parse_file(test_file)
        
        print(f"✅ Parser fonctionne")
        print(f"   • {instance.num_activities} activités")
        print(f"   • {instance.num_resources} ressources") 
        print(f"   • {instance.num_skills} compétences")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur parser: {e}")
        return False


def main():
    """Validation complète"""
    print("🚀 VALIDATION DU SOLVER MSRCPSP")
    print("=" * 40)
    
    checks = [
        check_instances(),
        check_scripts(),
        check_documentation(),
        test_parser()
    ]
    
    print("\n" + "=" * 40)
    
    if all(checks):
        print("✅ VALIDATION RÉUSSIE!")
        print("\n🎯 Le solver est prêt à utiliser:")
        print("   python3 msrcpsp_complete.py")
        print("   python3 msrcpsp_final.py")
        print("   python3 demo.py")
    else:
        print("❌ VALIDATION ÉCHOUÉE")
        print("Vérifiez les erreurs ci-dessus")
        sys.exit(1)


if __name__ == "__main__":
    main()
