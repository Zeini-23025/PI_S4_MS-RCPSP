
# Format des Données MSRCPSP (`.msrcp`)

Ce document décrit le format des fichiers `.msrcp` utilisés pour représenter des instances du problème d’ordonnancement de projets à ressources multiples et compétences multiples (MSRCPSP). Ce format est une extension du format de **Patterson** et permet de modéliser des projets avec des ressources ayant plusieurs compétences à différents niveaux.

---

## 📁 Structure Générale

Chaque fichier `.msrcp` est un fichier texte contenant plusieurs blocs :

---

## 1. 🧩 Project Module (Module du Projet)

### Ligne 1 :
```
nombre_activités  nombre_ressources  nombre_compétences  nombre_niveaux
```

### Ligne 2 :
```
Deadline de base (sans niveaux)
```

### Ligne 3 :
```
Deadline avec exigences de niveaux de compétence
```

### Lignes suivantes :  
Pour chaque activité (incluant les dummies "début" et "fin") :
```
durée  nombre_de_successeurs  ID_successeur_1  ID_successeur_2  ...
```

---

## 2. 👷 Workforce Module (Ressources humaines sans niveaux)

Chaque ligne correspond à une ressource :
```
1 ou 0 pour chaque type de compétence (1 = maîtrisée, 0 = non)
```

---

## 3. 🔢 Workforce Module avec Niveaux

Chaque ligne correspond à une ressource :
```
niveau_compétence_1  niveau_compétence_2  ... (0 = non maîtrisée)
```

---

## 4. 🎯 Skill Requirements Module (Exigences de compétences)

Chaque ligne correspond à une activité :
```
nb_ressources_compétence_1  nb_ressources_compétence_2  ...
```

---

## 5. 📈 Skill Level Requirements Module (Niveaux requis par compétence)

Chaque ligne correspond à une activité :
```
niveau_requis_compétence_1  niveau_requis_compétence_2  ...
```

---

## 6. 💰 Cost Module (Module de Coûts)

- Ligne 1 : Coût fixe minimal, coût variable minimal
- Lignes suivantes : coûts fixes puis coûts variables pour chaque type et niveau de compétence

---

## 7. 🔧 Common Resource Usage Module

- Taux de coût d'utilisation d’un bien commun
- Utilisation selon type de compétence et niveau

---

## 8. 🔁 Rework Module (Module de Re-travail)

Probabilité de devoir refaire le travail selon :
```
Type de compétence et niveau maîtrisé
```

---

## 🔚 Exemple Résumé

Exemple :
```
6 1 9
```
→ Activité de durée 6, avec un seul successeur : activité 9.

---

## 🔗 Source

Basé sur les spécifications du document :
> “Project Management with Dynamic Scheduling: Baseline Scheduling, Risk Analysis and Project Control”

Plus d'informations : [projectmanagement.ugent.be](http://www.projectmanagement.ugent.be/research/data)
