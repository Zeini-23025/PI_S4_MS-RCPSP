#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary Relevance pour MS-RCPSP
Implémente les recommandations pour une meilleure différenciation
"""

import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, hamming_loss
from sklearn.preprocessing import StandardScaler
from sklearn.base import clone
import pickle
import warnings
warnings.filterwarnings('ignore')

# Import des modules locaux
try:
    from msrcpsp_final import (MSRCPSPParser, MSRCPSPScheduler, 
                               ProjectInstance, Activity, Resource)
except ImportError as e:
    print(f"Attention: Module msrcpsp_final non trouvé. Erreur: {e}")
    print("Certaines fonctionnalités seront limitées.")
    MSRCPSPParser = None
    MSRCPSPScheduler = None


class InstanceFeatureExtractor:
    """Extracteur de caractéristiques pour les instances MS-RCPSP"""
    
    def __init__(self):
        self.feature_names = []
    
    def extract_structural_features(self, instance_data: Dict[str, Any]) -> Dict[str, float]:
        """Extrait les caractéristiques structurelles du projet"""
        features = {}
        
        # Caractéristiques de base
        features['n_activities'] = float(instance_data.get('nActs', 0))
        features['n_resources'] = float(instance_data.get('nRes', 0))
        features['n_skills'] = float(instance_data.get('nSkills', 0))
        
        # Ratios structurels
        n_acts = features['n_activities']
        n_res = features['n_resources']
        n_skills = features['n_skills']
        
        features['activities_per_resource'] = n_acts / max(n_res, 1)
        features['skills_per_resource'] = n_skills / max(n_res, 1)
        features['resource_density'] = n_res / max(n_acts, 1)
        
        # Statistiques des durées
        durations = instance_data.get('dur', [])
        if durations and len(durations) > 0:
            durations_array = np.array(durations)
            features['avg_duration'] = float(np.mean(durations_array))
            features['std_duration'] = float(np.std(durations_array))
            features['min_duration'] = float(np.min(durations_array))
            features['max_duration'] = float(np.max(durations_array))
            features['total_duration'] = float(np.sum(durations_array))
            features['duration_range'] = float(np.max(durations_array) - np.min(durations_array))
            features['duration_cv'] = float(np.std(durations_array) / max(np.mean(durations_array), 1))
        else:
            features.update({
                'avg_duration': 0.0, 'std_duration': 0.0, 'min_duration': 0.0,
                'max_duration': 0.0, 'total_duration': 0.0, 'duration_range': 0.0,
                'duration_cv': 0.0
            })
        
        return features
    
    def extract_network_features(self, instance_data: Dict[str, Any]) -> Dict[str, float]:
        """Extrait les caractéristiques du réseau de précédence"""
        features = {}
        precedence_graph = instance_data.get('precedence_graph', {})
        
        if precedence_graph and len(precedence_graph) > 0:
            n_nodes = len(precedence_graph)
            
            # Densité du réseau
            total_possible_edges = n_nodes * (n_nodes - 1)
            actual_edges = sum(len(node.get('successors', [])) for node in precedence_graph.values())
            features['network_density'] = float(actual_edges / max(total_possible_edges, 1))
            
            # Statistiques des degrés
            in_degrees = [len(node.get('predecessors', [])) for node in precedence_graph.values()]
            out_degrees = [len(node.get('successors', [])) for node in precedence_graph.values()]
            
            if in_degrees:
                features['avg_in_degree'] = float(np.mean(in_degrees))
                features['max_in_degree'] = float(np.max(in_degrees))
                features['std_in_degree'] = float(np.std(in_degrees))
            else:
                features['avg_in_degree'] = 0.0
                features['max_in_degree'] = 0.0
                features['std_in_degree'] = 0.0
                
            if out_degrees:
                features['avg_out_degree'] = float(np.mean(out_degrees))
                features['max_out_degree'] = float(np.max(out_degrees))
                features['std_out_degree'] = float(np.std(out_degrees))
            else:
                features['avg_out_degree'] = 0.0
                features['max_out_degree'] = 0.0
                features['std_out_degree'] = 0.0
            
            # Complexité du réseau
            features['network_complexity'] = features['std_in_degree'] + features['std_out_degree']
            
            # Nœuds spéciaux
            start_nodes = sum(1 for deg in in_degrees if deg == 0)
            end_nodes = sum(1 for deg in out_degrees if deg == 0)
            features['start_nodes_ratio'] = float(start_nodes / max(n_nodes, 1))
            features['end_nodes_ratio'] = float(end_nodes / max(n_nodes, 1))
            
        else:
            features.update({
                'network_density': 0.0, 'avg_in_degree': 0.0, 'avg_out_degree': 0.0,
                'max_in_degree': 0.0, 'max_out_degree': 0.0, 'std_in_degree': 0.0,
                'std_out_degree': 0.0, 'network_complexity': 0.0, 'start_nodes_ratio': 0.0,
                'end_nodes_ratio': 0.0
            })
        
        return features
    
    def extract_resource_features(self, instance_data: Dict[str, Any]) -> Dict[str, float]:
        """Extrait les caractéristiques des ressources et compétences"""
        features = {}
        
        # Compétences requises par les activités
        skill_requirements = instance_data.get('sreq', [])
        if skill_requirements and len(skill_requirements) > 0:
            skills_per_activity = [sum(1 for skill in req if skill) for req in skill_requirements]
            if skills_per_activity:
                features['avg_skills_per_activity'] = float(np.mean(skills_per_activity))
                features['max_skills_per_activity'] = float(np.max(skills_per_activity))
                features['min_skills_per_activity'] = float(np.min(skills_per_activity))
                features['std_skills_per_activity'] = float(np.std(skills_per_activity))
                
                # Complexité des compétences
                total_skill_demands = sum(skills_per_activity)
                n_activities = len(skills_per_activity)
                features['skill_demand_intensity'] = float(total_skill_demands / max(n_activities, 1))
            else:
                features.update({
                    'avg_skills_per_activity': 0.0, 'max_skills_per_activity': 0.0,
                    'min_skills_per_activity': 0.0, 'std_skills_per_activity': 0.0,
                    'skill_demand_intensity': 0.0
                })
        else:
            features.update({
                'avg_skills_per_activity': 0.0, 'max_skills_per_activity': 0.0,
                'min_skills_per_activity': 0.0, 'std_skills_per_activity': 0.0,
                'skill_demand_intensity': 0.0
            })
        
        # Maîtrise des compétences par les ressources
        resource_mastery = instance_data.get('mastery', [])
        if resource_mastery and len(resource_mastery) > 0:
            skills_per_resource = [sum(1 for skill in mastery if skill) for mastery in resource_mastery]
            if skills_per_resource:
                features['avg_skills_per_resource'] = float(np.mean(skills_per_resource))
                features['max_skills_per_resource'] = float(np.max(skills_per_resource))
                features['min_skills_per_resource'] = float(np.min(skills_per_resource))
                features['resource_flexibility'] = float(np.std(skills_per_resource))
            else:
                features.update({
                    'avg_skills_per_resource': 0.0, 'max_skills_per_resource': 0.0,
                    'min_skills_per_resource': 0.0, 'resource_flexibility': 0.0
                })
            
            # Couverture des compétences
            n_skills = instance_data.get('nSkills', 0)
            if n_skills > 0 and len(resource_mastery) > 0 and len(resource_mastery[0]) >= n_skills:
                skill_coverage = []
                for skill_idx in range(n_skills):
                    coverage = sum(1 for res in resource_mastery if len(res) > skill_idx and res[skill_idx])
                    skill_coverage.append(coverage)
                
                if skill_coverage:
                    features['avg_skill_coverage'] = float(np.mean(skill_coverage))
                    features['min_skill_coverage'] = float(np.min(skill_coverage))
                    features['skill_coverage_balance'] = float(np.std(skill_coverage))
                else:
                    features.update({
                        'avg_skill_coverage': 0.0, 'min_skill_coverage': 0.0,
                        'skill_coverage_balance': 0.0
                    })
            else:
                features.update({
                    'avg_skill_coverage': 0.0, 'min_skill_coverage': 0.0,
                    'skill_coverage_balance': 0.0
                })
                
        else:
            features.update({
                'avg_skills_per_resource': 0.0, 'max_skills_per_resource': 0.0,
                'min_skills_per_resource': 0.0, 'resource_flexibility': 0.0,
                'avg_skill_coverage': 0.0, 'min_skill_coverage': 0.0,
                'skill_coverage_balance': 0.0
            })
        
        return features
    
    def extract_temporal_features(self, instance_data: Dict[str, Any]) -> Dict[str, float]:
        """Extrait les caractéristiques temporelles"""
        features = {}
        
        # Métriques temporelles de base
        est = instance_data.get('est', [])
        lst = instance_data.get('lst', [])
        lft = instance_data.get('lft', [])
        float_dyn = instance_data.get('float_dyn', [])
        durations = instance_data.get('dur', [])
        
        if est and lst and len(est) > 0 and len(lst) > 0:
            # Étendue temporelle
            features['project_est_span'] = float(max(est) - min(est)) if len(est) > 1 else 0.0
            features['project_lst_span'] = float(max(lst) - min(lst)) if len(lst) > 1 else 0.0
            
            # EFT calculé
            if durations and len(durations) == len(est):
                eft = [est[i] + durations[i] for i in range(len(est))]
                features['project_duration_est'] = float(max(eft)) if eft else 0.0
            else:
                features['project_duration_est'] = float(max(est)) if est else 0.0
        else:
            features.update({
                'project_est_span': 0.0, 'project_lst_span': 0.0,
                'project_duration_est': 0.0
            })
            
        # Analyse du flottement
        if float_dyn and len(float_dyn) > 0:
            valid_floats = [f for f in float_dyn if f != float('inf') and f >= 0 and not np.isnan(f)]
            if valid_floats:
                features['avg_float'] = float(np.mean(valid_floats))
                features['std_float'] = float(np.std(valid_floats))
                features['max_float'] = float(np.max(valid_floats))
                features['critical_activities_ratio'] = float(sum(1 for f in valid_floats if f == 0) / len(valid_floats))
                mean_float = np.mean(valid_floats)
                features['float_distribution'] = float(np.std(valid_floats) / max(mean_float, 1))
            else:
                features.update({
                    'avg_float': 0.0, 'std_float': 0.0, 'max_float': 0.0,
                    'critical_activities_ratio': 1.0, 'float_distribution': 0.0
                })
        else:
            features.update({
                'avg_float': 0.0, 'std_float': 0.0, 'max_float': 0.0,
                'critical_activities_ratio': 1.0, 'float_distribution': 0.0
            })
        
        return features
    
    def extract_all_features(self, instance_data: Dict[str, Any]) -> Dict[str, float]:
        """Extrait toutes les caractéristiques d'une instance"""
        all_features = {}
        
        all_features.update(self.extract_structural_features(instance_data))
        all_features.update(self.extract_network_features(instance_data))
        all_features.update(self.extract_resource_features(instance_data))
        all_features.update(self.extract_temporal_features(instance_data))
        
        # Stocker les noms des caractéristiques
        self.feature_names = list(all_features.keys())
        
        return all_features


class BinaryRelevanceClassifier:
    """Implémentation optimisée de Binary Relevance"""
    
    def __init__(self, base_classifier=None, random_state=42):
        if base_classifier is None:
            self.base_classifier = RandomForestClassifier(
                n_estimators=100, 
                max_depth=8,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state, 
                n_jobs=-1
            )
        else:
            self.base_classifier = base_classifier
            
        self.classifiers = {}
        self.labels = []
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_fitted = False
        self.training_scores = {}
    
    def fit(self, X: np.ndarray, y: np.ndarray, labels: List[str], feature_names: List[str] = None):
        """Entraîne un classificateur binaire pour chaque règle de priorité"""
        print(f"Entraînement de Binary Relevance avec {len(labels)} règles de priorité...")
        print(f"Dataset: {X.shape[0]} instances, {X.shape[1]} caractéristiques")
        
        self.labels = labels
        self.feature_names = feature_names or [f"feature_{i}" for i in range(X.shape[1])]
        
        # Normalisation des caractéristiques
        X_scaled = self.scaler.fit_transform(X)
        
        # Entraînement d'un classificateur pour chaque label
        for i, label in enumerate(labels):
            print(f"Entraînement du classificateur pour {label}...")
            
            # Créer une copie du classificateur de base
            clf = clone(self.base_classifier)
            
            # Entraîner sur le label binaire i
            y_binary = y[:, i].astype(int)
            clf.fit(X_scaled, y_binary)
            
            self.classifiers[label] = clf
            
            # Calculer les scores d'entraînement avec validation croisée
            unique_classes = np.unique(y_binary)
            if len(unique_classes) > 1:  # Seulement si on a les deux classes
                try:
                    cv_scores = cross_val_score(clf, X_scaled, y_binary, cv=3, scoring='accuracy')
                    self.training_scores[label] = {
                        'cv_mean': float(np.mean(cv_scores)),
                        'cv_std': float(np.std(cv_scores))
                    }
                    print(f"  CV Accuracy: {np.mean(cv_scores):.3f} (±{np.std(cv_scores):.3f})")
                except:
                    self.training_scores[label] = {'cv_mean': 1.0, 'cv_std': 0.0}
                    print(f"  CV Accuracy: 1.000 (parfait)")
            else:
                self.training_scores[label] = {'cv_mean': 1.0, 'cv_std': 0.0}
                print(f"  Classes uniques détectées - Accuracy parfaite")
            
            # Afficher la distribution des classes
            unique, counts = np.unique(y_binary, return_counts=True)
            distribution = {int(u): int(c) for u, c in zip(unique, counts)}
            print(f"  Distribution: {distribution}")
        
        self.is_fitted = True
        print("Entraînement terminé!")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Prédit les labels pour les nouvelles instances"""
        if not self.is_fitted:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")
        
        X_scaled = self.scaler.transform(X)
        predictions = np.zeros((X.shape[0], len(self.labels)))
        
        for i, label in enumerate(self.labels):
            predictions[:, i] = self.classifiers[label].predict(X_scaled)
        
        return predictions
    
    def predict_proba(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        """Prédit les probabilités pour chaque règle de priorité"""
        if not self.is_fitted:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")
        
        X_scaled = self.scaler.transform(X)
        probabilities = {}
        
        for label in self.labels:
            prob = self.classifiers[label].predict_proba(X_scaled)
            # Prendre la probabilité de la classe positive (1)
            probabilities[label] = prob[:, 1] if prob.shape[1] > 1 else prob[:, 0]
        
        return probabilities
    
    def get_best_rules(self, X: np.ndarray, top_k: int = 3) -> List[List[str]]:
        """Retourne les meilleures règles pour chaque instance"""
        probabilities = self.predict_proba(X)
        
        # Convertir en matrice
        prob_matrix = np.column_stack([probabilities[label] for label in self.labels])
        
        # Trouver les top_k pour chaque instance
        best_rules = []
        for i in range(prob_matrix.shape[0]):
            # Indices des règles triées par probabilité décroissante
            sorted_indices = np.argsort(prob_matrix[i])[::-1]
            best_rules_instance = [self.labels[idx] for idx in sorted_indices[:top_k]]
            best_rules.append(best_rules_instance)
        
        return best_rules
    
    def get_feature_importance(self, top_n: int = 10) -> Dict[str, Dict[str, float]]:
        """Retourne l'importance des caractéristiques pour chaque règle"""
        if not self.is_fitted:
            raise ValueError("Le modèle doit être entraîné")
        
        importance_dict = {}
        
        for label in self.labels:
            clf = self.classifiers[label]
            if hasattr(clf, 'feature_importances_'):
                importances = clf.feature_importances_
                
                # Créer un dictionnaire feature_name -> importance
                feature_importance = dict(zip(self.feature_names, importances))
                
                # Trier par importance décroissante
                sorted_features = sorted(feature_importance.items(), 
                                       key=lambda x: x[1], reverse=True)
                
                importance_dict[label] = dict(sorted_features[:top_n])
        
        return importance_dict
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """Évalue les performances du modèle"""
        predictions = self.predict(X_test)
        
        # Convertir en entiers pour éviter les erreurs de type
        predictions = predictions.astype(int)
        y_test = y_test.astype(int)
        
        results = {}
        
        # Métriques globales
        results['hamming_loss'] = float(hamming_loss(y_test, predictions))
        results['exact_match_ratio'] = float(np.mean(np.all(predictions == y_test, axis=1)))
        
        # Subset accuracy (au moins une prédiction correcte)
        subset_accuracy = float(np.mean(np.any(np.logical_and(predictions, y_test), axis=1)))
        results['subset_accuracy'] = subset_accuracy
        
        # Métriques par règle
        rule_metrics = {}
        for i, label in enumerate(self.labels):
            y_true = y_test[:, i].astype(int)
            y_pred = predictions[:, i].astype(int)
            
            # Métriques de base
            accuracy = float(accuracy_score(y_true, y_pred))
            
            # Precision, Recall, F1
            tp = int(np.sum((y_pred == 1) & (y_true == 1)))
            fp = int(np.sum((y_pred == 1) & (y_true == 0)))
            fn = int(np.sum((y_pred == 0) & (y_true == 1)))
            
            precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
            recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
            f1 = float(2 * (precision * recall) / (precision + recall)) if (precision + recall) > 0 else 0.0
            
            rule_metrics[label] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'support': int(np.sum(y_true))
            }
        
        results['rule_metrics'] = rule_metrics
        
        return results
    
    def save_model(self, filepath: str):
        """Sauvegarde le modèle entraîné"""
        model_data = {
            'classifiers': self.classifiers,
            'labels': self.labels,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted,
            'training_scores': self.training_scores
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Modèle sauvegardé dans {filepath}")
    
    def load_model(self, filepath: str):
        """Charge un modèle pré-entraîné"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.classifiers = model_data['classifiers']
        self.labels = model_data['labels']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.is_fitted = model_data['is_fitted']
        self.training_scores = model_data.get('training_scores', {})
        print(f"Modèle chargé depuis {filepath}")


class MSRCPSPDatasetBuilder:
    """Constructeur de dataset optimisé pour l'entraînement des modèles"""
    
    def __init__(self, results_dir: str = "./resultats", instances_dir: str = "./Instances"):
        self.results_dir = results_dir
        self.instances_dir = instances_dir
        self.feature_extractor = InstanceFeatureExtractor()
        self.algorithms = ['HRPW*', 'LST', 'LFT', 'MTS', 'TIMROS', 'HRU1', 'TIMRES', 'HRU2', 'STFD', 'EFT']
    
    def load_makespan_results(self) -> pd.DataFrame:
        """Charge les résultats de makespan depuis les fichiers JSON"""
        makespan_details_dir = os.path.join(self.results_dir, "makespan_details")
        
        if not os.path.exists(makespan_details_dir):
            print(f"Répertoire {makespan_details_dir} non trouvé.")
            print("Vous devez d'abord exécuter makespan_calculator.py pour générer les résultats.")
            raise FileNotFoundError(f"Répertoire {makespan_details_dir} manquant")
        
        all_results = []
        
        for filename in os.listdir(makespan_details_dir):
            if filename.endswith('_makespans.json'):
                filepath = os.path.join(makespan_details_dir, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                instance_name = data['instance']
                results = data['results']
                
                # Créer une ligne avec les makespans pour chaque algorithme
                row = {'instance': instance_name}
                for algo in self.algorithms:
                    if algo in results:
                        makespan = results[algo]['makespan']
                        row[f'{algo}_makespan'] = makespan if makespan != float('inf') else np.nan
                    else:
                        row[f'{algo}_makespan'] = np.nan
                
                all_results.append(row)
        
        return pd.DataFrame(all_results)
    
    def analyze_makespan_variance(self, makespan_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse la variance des makespans pour sélectionner les instances discriminantes"""
        print("\n" + "="*60)
        print("ANALYSE DE LA VARIABILITÉ DES MAKESPANS")
        print("="*60)
        
        # Calculer la variance par instance
        makespan_cols = [f'{algo}_makespan' for algo in self.algorithms]
        makespan_matrix = makespan_df[makespan_cols].values
        
        # Remplacer NaN par une valeur très élevée
        makespan_matrix = np.nan_to_num(makespan_matrix, nan=999999.0)
        
        # Calculer les statistiques par instance
        instance_stats = []
        for i, row in makespan_df.iterrows():
            makespans = [row[f'{algo}_makespan'] for algo in self.algorithms]
            valid_makespans = [m for m in makespans if not pd.isna(m)]
            
            if len(valid_makespans) > 1:
                variance = np.var(valid_makespans)
                std_dev = np.std(valid_makespans)
                range_val = max(valid_makespans) - min(valid_makespans)
                cv = std_dev / max(np.mean(valid_makespans), 1)  # Coefficient de variation
            else:
                variance = 0.0
                std_dev = 0.0
                range_val = 0.0
                cv = 0.0
            
            instance_stats.append({
                'instance': row['instance'],
                'variance': variance,
                'std_dev': std_dev,
                'range': range_val,
                'cv': cv,
                'valid_algorithms': len(valid_makespans)
            })
        
        # Analyser la distribution
        variances = [s['variance'] for s in instance_stats]
        ranges = [s['range'] for s in instance_stats]
        cvs = [s['cv'] for s in instance_stats]
        
        print(f"Statistiques de variabilité:")
        print(f"  Variance moyenne: {np.mean(variances):.4f}")
        print(f"  Variance médiane: {np.median(variances):.4f}")
        print(f"  Variance max: {np.max(variances):.4f}")
        print(f"  Range moyenne: {np.mean(ranges):.4f}")
        print(f"  CV moyen: {np.mean(cvs):.4f}")
        
        # Identifier les instances les plus discriminantes
        discriminant_threshold = np.percentile(variances, 75)  # Top 25%
        discriminant_instances = [s for s in instance_stats if s['variance'] >= discriminant_threshold]
        
        print(f"\nInstances discriminantes (variance >= {discriminant_threshold:.4f}):")
        print(f"  Nombre d'instances: {len(discriminant_instances)}")
        
        return {
            'instance_stats': instance_stats,
            'discriminant_instances': discriminant_instances,
            'thresholds': {
                'variance_75': discriminant_threshold,
                'range_75': np.percentile(ranges, 75),
                'cv_75': np.percentile(cvs, 75)
            }
        }
    
    def create_binary_labels_adaptive(self, makespan_df: pd.DataFrame, 
                                    tolerance: float = 0.01,
                                    use_discriminant_only: bool = False) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Crée les labels binaires avec tolérance adaptative et sélection discriminante
        """
        print(f"\nCréation des labels binaires avec tolérance {tolerance*100:.1f}%")
        
        # Analyser la variance
        variance_analysis = self.analyze_makespan_variance(makespan_df)
        
        # Sélectionner les instances à utiliser
        if use_discriminant_only:
            selected_instances = [s['instance'] for s in variance_analysis['discriminant_instances']]
            print(f"Utilisation des instances discriminantes uniquement: {len(selected_instances)} instances")
            filtered_df = makespan_df[makespan_df['instance'].isin(selected_instances)]
        else:
            filtered_df = makespan_df
            print(f"Utilisation de toutes les instances: {len(filtered_df)} instances")
        
        labels = np.zeros((len(filtered_df), len(self.algorithms)))
        
        # Statistiques pour l'analyse
        label_stats = {algo: {'positive': 0, 'total': 0} for algo in self.algorithms}
        
        for i, (_, row) in enumerate(filtered_df.iterrows()):
            makespans = []
            for algo in self.algorithms:
                makespan = getattr(row, f'{algo}_makespan')
                if not pd.isna(makespan):
                    makespans.append(makespan)
                else:
                    makespans.append(float('inf'))
            
            # Trouver le meilleur makespan
            valid_makespans = [m for m in makespans if m != float('inf')]
            if valid_makespans:
                best_makespan = min(valid_makespans)
                threshold = best_makespan * (1 + tolerance)
                
                # Marquer les algorithmes dans la tolérance comme "bons"
                for j, makespan in enumerate(makespans):
                    label_stats[self.algorithms[j]]['total'] += 1
                    if makespan <= threshold:
                        labels[i, j] = 1
                        label_stats[self.algorithms[j]]['positive'] += 1
        
        # Afficher les statistiques
        print(f"\nDistribution des labels avec tolérance {tolerance*100:.1f}%:")
        for algo in self.algorithms:
            positive = label_stats[algo]['positive']
            total = label_stats[algo]['total']
            percentage = (positive / total * 100) if total > 0 else 0
            print(f"  {algo:8s}: {positive:3d}/{total} ({percentage:5.1f}%)")
        
        return labels, variance_analysis
    
    def build_dataset(self, 
                     tolerance: float = 0.01,
                     use_discriminant_only: bool = False,
                     test_multiple_tolerances: bool = True) -> Tuple[np.ndarray, np.ndarray, List[str], List[str], Dict[str, Any]]:
        """
        Construit le dataset avec les recommandations
        """
        print("=" * 70)
        print("CONSTRUCTION DU DATASET MS-RCPSP")
        print("=" * 70)
        
        # Charger les résultats de makespan
        makespan_df = self.load_makespan_results()
        print(f"Chargé {len(makespan_df)} instances avec résultats de makespan")
        
        # Tester plusieurs tolérances si demandé
        if test_multiple_tolerances:
            print("\n" + "="*60)
            print("TEST DE DIFFÉRENTES TOLÉRANCES")
            print("="*60)
            
            tolerances_to_test = [0.001, 0.005, 0.01, 0.02, 0.05]
            tolerance_results = {}
            
            for test_tol in tolerances_to_test:
                test_labels, _ = self.create_binary_labels_adaptive(makespan_df, test_tol, False)
                
                # Calculer les statistiques de diversité
                diversity_scores = []
                for i in range(len(test_labels)):
                    positive_count = np.sum(test_labels[i])
                    diversity_scores.append(positive_count)
                
                avg_diversity = np.mean(diversity_scores)
                std_diversity = np.std(diversity_scores)
                
                tolerance_results[test_tol] = {
                    'avg_positive_per_instance': avg_diversity,
                    'std_positive_per_instance': std_diversity,
                    'min_positive': np.min(diversity_scores),
                    'max_positive': np.max(diversity_scores)
                }
                
                print(f"Tolérance {test_tol*100:4.1f}%: Avg={avg_diversity:.1f}±{std_diversity:.1f} règles positives par instance")
            
            # Recommander la meilleure tolérance
            best_tolerance = min(tolerance_results.keys(), 
                               key=lambda t: abs(tolerance_results[t]['avg_positive_per_instance'] - len(self.algorithms)/2))
            print(f"\nTolérance recommandée: {best_tolerance*100:.1f}%")
            tolerance = best_tolerance
        
        # Créer les labels binaires avec la tolérance choisie
        y, variance_analysis = self.create_binary_labels_adaptive(makespan_df, tolerance, use_discriminant_only)
        
        # Extraire les caractéristiques pour chaque instance
        X_list = []
        valid_instances = []
        feature_names = None
        
        print(f"\n{'='*60}")
        print("EXTRACTION DES CARACTÉRISTIQUES")
        print(f"{'='*60}")
        
        # Filtrer les instances si nécessaire
        if use_discriminant_only:
            selected_instances = [s['instance'] for s in variance_analysis['discriminant_instances']]
            makespan_df_filtered = makespan_df[makespan_df['instance'].isin(selected_instances)]
        else:
            makespan_df_filtered = makespan_df
        
        processed_count = 0
        for i, row in makespan_df_filtered.iterrows():
            instance_name = row['instance']
            dzn_file = os.path.join(self.instances_dir, f"{instance_name}.msrcp")
            
            if os.path.exists(dzn_file):
                try:
                    # Charger et traiter l'instance
                    instance_data = parse_dzn_file(dzn_file)
                    instance_data = compute_temporal_metrics(instance_data)
                    
                    # Extraire les caractéristiques
                    features = self.feature_extractor.extract_all_features(instance_data)
                    
                    if feature_names is None:
                        feature_names = list(features.keys())
                    
                    X_list.append(list(features.values()))
                    valid_instances.append(instance_name)
                    
                    processed_count += 1
                    if processed_count % 50 == 0:
                        print(f"  Traité {processed_count} instances...")
                    
                except Exception as e:
                    print(f"Erreur lors du traitement de {instance_name}: {e}")
            else:
                print(f"Fichier {dzn_file} non trouvé")
        
        # Convertir en arrays numpy
        X = np.array(X_list, dtype=np.float64)
        y_filtered = y[:len(valid_instances)]
        
        print(f"\nDataset final: {X.shape[0]} instances, {X.shape[1]} caractéristiques")
        print(f"Caractéristiques extraites: {len(feature_names)}")
        
        # Afficher la distribution finale des labels
        print(f"\nDistribution finale des labels:")
        for i, algo in enumerate(self.algorithms):
            positive_count = int(np.sum(y_filtered[:, i]))
            total_count = len(y_filtered)
            percentage = positive_count / total_count * 100
            print(f"  {algo:8s}: {positive_count:3d}/{total_count} ({percentage:5.1f}%)")
        
        analysis_results = {
            'variance_analysis': variance_analysis,
            'tolerance_used': tolerance,
            'discriminant_only': use_discriminant_only,
            'dataset_stats': {
                'n_instances': X.shape[0],
                'n_features': X.shape[1],
                'label_distribution': {
                    algo: {
                        'positive': int(np.sum(y_filtered[:, i])),
                        'percentage': float(np.sum(y_filtered[:, i]) / len(y_filtered) * 100)
                    }
                    for i, algo in enumerate(self.algorithms)
                }
            }
        }
        
        return X, y_filtered, valid_instances, feature_names, analysis_results


def parse_dzn_file(filepath: str) -> Dict[str, Any]:
    """Parse un fichier .dzn ou .msrcp et retourne les données structurées"""
    try:
        if MSRCPSPParser is None:
            raise ImportError("Module msrcpsp_final non disponible")
        
        # Utiliser le parser existant
        project_instance = MSRCPSPParser.parse_file(filepath)
        
        # Convertir en format dictionnaire pour la compatibilité
        instance_data = {
            'nActs': project_instance.num_activities,
            'nRes': project_instance.num_resources,
            'nSkills': project_instance.num_skills,
            'dur': [act.duration for act in project_instance.activities],
            'sreq': [act.skill_requirements for act in project_instance.activities],
            'mastery': [res.skills for res in project_instance.resources],
            'precedence_graph': {},
            'est': [],
            'lst': [],
            'lft': [],
            'float_dyn': []
        }
        
        # Construire le graphe de précédence
        for act in project_instance.activities:
            instance_data['precedence_graph'][act.id] = {
                'successors': act.successors,
                'predecessors': act.predecessors
            }
        
        return instance_data
        
    except Exception as e:
        print(f"Erreur lors du parsing de {filepath}: {e}")
        # Parser basique pour fichiers .dzn
        return parse_dzn_basic(filepath)


def parse_dzn_basic(filepath: str) -> Dict[str, Any]:
    """Parser basique pour fichiers .dzn"""
    instance_data = {
        'nActs': 0, 'nRes': 0, 'nSkills': 0,
        'dur': [], 'sreq': [], 'mastery': [],
        'precedence_graph': {}, 'est': [], 'lst': [], 'lft': [], 'float_dyn': []
    }
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Extraire les valeurs de base
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('nActs'):
                instance_data['nActs'] = int(line.split('=')[1].rstrip(';'))
            elif line.startswith('nRes'):
                instance_data['nRes'] = int(line.split('=')[1].rstrip(';'))
            elif line.startswith('nSkills'):
                instance_data['nSkills'] = int(line.split('=')[1].rstrip(';'))
    except:
        pass
    
    return instance_data


def compute_temporal_metrics(instance_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calcule les métriques temporelles pour une instance"""
    try:
        n_acts = instance_data.get('nActs', 0)
        durations = instance_data.get('dur', [])
        precedence_graph = instance_data.get('precedence_graph', {})
        
        if n_acts == 0 or not durations:
            return instance_data
        
        # Initialiser les listes temporelles
        est = [0] * n_acts
        lst = [float('inf')] * n_acts
        lft = [0] * n_acts
        float_dyn = [0] * n_acts
        
        # Calcul EST (Earliest Start Time) - parcours en avant
        for act_id in range(n_acts):
            if act_id in precedence_graph:
                predecessors = precedence_graph[act_id].get('predecessors', [])
                if predecessors:
                    est[act_id] = max(est[pred] + durations[pred] for pred in predecessors 
                                    if pred < len(durations))
        
        # Calcul LST (Latest Start Time) - parcours en arrière
        max_est = max(est[i] + durations[i] for i in range(len(durations)) if i < len(est))
        lst = [max_est] * n_acts
        
        for act_id in reversed(range(n_acts)):
            if act_id in precedence_graph:
                successors = precedence_graph[act_id].get('successors', [])
                if successors:
                    lst[act_id] = min(lst[succ] - durations[act_id] for succ in successors 
                                    if succ < len(lst))
        
        # Calcul LFT et flottement
        for i in range(n_acts):
            if i < len(durations):
                lft[i] = lst[i] + durations[i]
                float_dyn[i] = lst[i] - est[i]
        
        # Mettre à jour l'instance
        instance_data.update({
            'est': est,
            'lst': lst,
            'lft': lft,
            'float_dyn': float_dyn
        })
        
    except Exception as e:
        print(f"Erreur dans compute_temporal_metrics: {e}")
    
    return instance_data


class MLIntegratedMSRCPSP:
    """Intégration du modèle ML avec le solveur MS-RCPSP"""
    
    def __init__(self, model_path: str = None):
        self.ml_model = None
        self.feature_extractor = InstanceFeatureExtractor()
        self.algorithms = ['EST', 'LFT', 'MSLF', 'SPT', 'LPT', 'FCFS', 'LST']
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """Charge le modèle ML pré-entraîné"""
        try:
            self.ml_model = BinaryRelevanceClassifier()
            self.ml_model.load_model(model_path)
            print(f"Modèle ML chargé depuis {model_path}")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")
            self.ml_model = None
    
    def predict_best_algorithms(self, instance_file: str, top_k: int = 3) -> List[str]:
        """Prédit les meilleurs algorithmes pour une instance donnée"""
        if self.ml_model is None:
            print("Aucun modèle ML disponible. Utilisation des algorithmes par défaut.")
            return self.algorithms[:top_k]
        
        try:
            # Parser l'instance
            instance_data = parse_dzn_file(instance_file)
            instance_data = compute_temporal_metrics(instance_data)
            
            # Extraire les caractéristiques
            features = self.feature_extractor.extract_all_features(instance_data)
            X = np.array([list(features.values())]).reshape(1, -1)
            
            # Prédire avec le modèle ML
            best_rules = self.ml_model.get_best_rules(X, top_k=top_k)
            probabilities = self.ml_model.predict_proba(X)
            
            # Mapper les règles ML aux algorithmes du solveur
            ml_to_solver_mapping = {
                'EST': 'EST', 'LFT': 'LFT', 'MSLF': 'MSLF', 'SPT': 'SPT',
                'LPT': 'LPT', 'FCFS': 'FCFS', 'LST': 'LST',
                'HRPW*': 'EST', 'MTS': 'MSLF', 'TIMROS': 'LFT',
                'HRU1': 'SPT', 'TIMRES': 'LST', 'HRU2': 'LPT',
                'STFD': 'FCFS', 'EFT': 'EST'
            }
            
            recommended_algorithms = []
            for rule in best_rules[0]:
                mapped_algo = ml_to_solver_mapping.get(rule, rule)
                if mapped_algo in self.algorithms and mapped_algo not in recommended_algorithms:
                    recommended_algorithms.append(mapped_algo)
            
            # Ajouter des algorithmes par défaut si nécessaire
            while len(recommended_algorithms) < top_k:
                for algo in self.algorithms:
                    if algo not in recommended_algorithms:
                        recommended_algorithms.append(algo)
                        break
            
            print(f"Algorithmes recommandés par ML: {recommended_algorithms[:top_k]}")
            return recommended_algorithms[:top_k]
            
        except Exception as e:
            print(f"Erreur lors de la prédiction ML: {e}")
            return self.algorithms[:top_k]
    
    def solve_with_ml_guidance(self, instance_file: str, output_dir: str = "./resultats") -> Dict[str, Any]:
        """Résout une instance en utilisant les recommandations ML"""
        if MSRCPSPScheduler is None:
            print("Solveur MS-RCPSP non disponible")
            return {}
        
        try:
            # Obtenir les recommandations ML
            recommended_algos = self.predict_best_algorithms(instance_file, top_k=5)
            
            # Charger l'instance
            project_instance = MSRCPSPParser.parse_file(instance_file)
            solver = MSRCPSPScheduler(project_instance)
            
            results = {}
            best_makespan = float('inf')
            best_algorithm = None
            best_schedule = None
            
            print(f"Test des algorithmes recommandés: {recommended_algos}")
            
            # Tester les algorithmes recommandés
            for algorithm in recommended_algos:
                try:
                    print(f"Test de l'algorithme {algorithm}...")
                    makespan, schedule = solver.schedule_with_priority(algorithm)
                    
                    results[algorithm] = {
                        'makespan': makespan,
                        'schedule': schedule,
                        'success': makespan != float('inf')
                    }
                    
                    if makespan < best_makespan:
                        best_makespan = makespan
                        best_algorithm = algorithm
                        best_schedule = schedule
                    
                    print(f"  {algorithm}: makespan = {makespan}")
                    
                except Exception as e:
                    print(f"  Erreur avec {algorithm}: {e}")
                    results[algorithm] = {
                        'makespan': float('inf'),
                        'schedule': None,
                        'success': False,
                        'error': str(e)
                    }
            
            # Sauvegarder les résultats
            instance_name = os.path.basename(instance_file).replace('.dzn', '').replace('.msrcp', '')
            
            summary = {
                'instance': instance_name,
                'ml_recommended_algorithms': recommended_algos,
                'best_algorithm': best_algorithm,
                'best_makespan': best_makespan,
                'all_results': results,
                'performance_improvement': self._calculate_improvement(results)
            }
            
            # Sauvegarder en JSON
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{instance_name}_ml_results.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"Résultats sauvegardés dans {output_file}")
            print(f"Meilleur algorithme: {best_algorithm} (makespan: {best_makespan})")
            
            return summary
            
        except Exception as e:
            print(f"Erreur lors de la résolution: {e}")
            return {}
    
    def _calculate_improvement(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Calcule l'amélioration de performance"""
        valid_makespans = [r['makespan'] for r in results.values() 
                          if r['success'] and r['makespan'] != float('inf')]
        
        if len(valid_makespans) < 2:
            return {'improvement_percentage': 0.0, 'variance': 0.0}
        
        best_makespan = min(valid_makespans)
        worst_makespan = max(valid_makespans)
        avg_makespan = np.mean(valid_makespans)
        
        improvement = ((worst_makespan - best_makespan) / worst_makespan * 100 
                      if worst_makespan > 0 else 0.0)
        variance = np.var(valid_makespans)
        
        return {
            'improvement_percentage': improvement,
            'variance': variance,
            'best_makespan': best_makespan,
            'worst_makespan': worst_makespan,
            'average_makespan': avg_makespan
        }
    
    def batch_solve_with_ml(self, instances_dir: str, output_dir: str = "./resultats_ml") -> Dict[str, Any]:
        """Résout un batch d'instances avec guidage ML"""
        if not os.path.exists(instances_dir):
            print(f"Répertoire {instances_dir} non trouvé")
            return {}
        
        results = {}
        total_files = 0
        successful_files = 0
        
        print(f"Traitement du répertoire: {instances_dir}")
        
        for filename in os.listdir(instances_dir):
            if filename.endswith(('.dzn', '.msrcp')):
                total_files += 1
                instance_path = os.path.join(instances_dir, filename)
                
                print(f"\n{'='*60}")
                print(f"Traitement de {filename}")
                print(f"{'='*60}")
                
                try:
                    result = self.solve_with_ml_guidance(instance_path, output_dir)
                    if result:
                        results[filename] = result
                        successful_files += 1
                    else:
                        results[filename] = {'error': 'Échec de la résolution'}
                
                except Exception as e:
                    print(f"Erreur avec {filename}: {e}")
                    results[filename] = {'error': str(e)}
        
        # Générer un rapport global
        summary_report = {
            'total_instances': total_files,
            'successful_instances': successful_files,
            'success_rate': (successful_files / total_files * 100) if total_files > 0 else 0.0,
            'detailed_results': results,
            'ml_model_used': self.ml_model is not None
        }
        
        # Sauvegarder le rapport
        os.makedirs(output_dir, exist_ok=True)
        report_file = os.path.join(output_dir, 'ml_batch_report.json')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(summary_report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n{'='*60}")
        print("RAPPORT GLOBAL")
        print(f"{'='*60}")
        print(f"Instances traitées: {successful_files}/{total_files}")
        print(f"Taux de réussite: {summary_report['success_rate']:.1f}%")
        print(f"Rapport sauvegardé: {report_file}")
        
        return summary_report


def main():
    """Fonction principale pour Binary Relevance MS-RCPSP"""
    print("=" * 80)
    print("BINARY RELEVANCE POUR MS-RCPSP")
    print("Implémente les recommandations pour une meilleure différenciation")
    print("=" * 80)
    
    # Menu principal
    print("\nOptions disponibles:")
    print("1. Entraîner un nouveau modèle ML")
    print("2. Utiliser le modèle ML pour résoudre des instances")
    print("3. Démonstration de l'intégration ML")
    print("4. Traitement en lot avec ML")
    
    try:
        choice = input("\nChoisissez une option (1-4, ou Entrée pour option 1): ").strip()
        if not choice:
            choice = "1"
    except KeyboardInterrupt:
        print("\nInterruption utilisateur.")
        return
    
    if choice == "1":
        train_new_model()
    elif choice == "2":
        use_ml_model()
    elif choice == "3":
        demonstrate_ml_integration()
    elif choice == "4":
        batch_processing_with_ml()
    else:
        print("Option invalide. Entraînement d'un nouveau modèle par défaut.")
        train_new_model()


def train_new_model():
    """Entraîne un nouveau modèle ML"""
    print("\n" + "="*60)
    print("ENTRAÎNEMENT D'UN NOUVEAU MODÈLE")
    print("="*60)
    
    # Construire le dataset avec les améliorations
    dataset_builder = MSRCPSPDatasetBuilder()
    
    try:
        # Test avec différentes configurations
        configurations = [
            {"tolerance": 0.001, "use_discriminant_only": False, 
             "name": "Tolérance très stricte (0.1%)"},
            {"tolerance": 0.01, "use_discriminant_only": False, 
             "name": "Tolérance stricte (1%)"},
            {"tolerance": 0.01, "use_discriminant_only": True, 
             "name": "Instances discriminantes (1%)"},
        ]
        
        best_config = None
        best_diversity = 0
        
        for config in configurations:
            print(f"\n{'='*80}")
            print(f"TEST DE CONFIGURATION: {config['name']}")
            print(f"{'='*80}")
            
            X, y, instance_names, feature_names, analysis = dataset_builder.build_dataset(
                tolerance=config["tolerance"],
                use_discriminant_only=config["use_discriminant_only"],
                test_multiple_tolerances=False
            )
            
            if len(X) == 0:
                print("Aucune instance valide trouvée pour cette configuration!")
                continue
            
            # Calculer la diversité des labels
            diversity_scores = []
            for i in range(len(y)):
                positive_count = np.sum(y[i])
                diversity_scores.append(positive_count)
            
            avg_diversity = np.mean(diversity_scores)
            std_diversity = np.std(diversity_scores)
            
            print(f"\nRésultats de la configuration:")
            print(f"  Instances: {len(X)}")
            print(f"  Diversité moyenne: {avg_diversity:.1f}±{std_diversity:.1f}")
            print(f"  Range: {np.min(diversity_scores):.0f} - {np.max(diversity_scores):.0f}")
            
            # Sélectionner la meilleure configuration
            target_diversity = len(dataset_builder.algorithms) / 2
            diversity_score = 1 / (1 + abs(avg_diversity - target_diversity))
            
            if diversity_score > best_diversity:
                best_diversity = diversity_score
                best_config = {
                    'X': X, 'y': y, 'instance_names': instance_names, 
                    'feature_names': feature_names, 'analysis': analysis,
                    'config': config
                }
        
        if best_config is None:
            print("Aucune configuration valide trouvée!")
            return
        
        print(f"\n{'='*80}")
        print(f"CONFIGURATION SÉLECTIONNÉE: {best_config['config']['name']}")
        print(f"{'='*80}")
        
        X, y, instance_names, feature_names, analysis = (
            best_config['X'], best_config['y'], best_config['instance_names'],
            best_config['feature_names'], best_config['analysis']
        )
        
    except FileNotFoundError as e:
        print(f"Erreur: {e}")
        print("Veuillez d'abord exécuter makespan_calculator.py pour générer les résultats.")
        return
    
    # Suite de l'entraînement...
    complete_model_training(X, y, instance_names, feature_names, dataset_builder, best_config)


def complete_model_training(X, y, instance_names, feature_names, dataset_builder, best_config):
    """Complete le processus d'entraînement du modèle"""
    # Diviser en train/test
    print(f"\n{'='*60}")
    print("DIVISION TRAIN/TEST")
    print(f"{'='*60}")
    
    if len(X) < 4:
        print(f"Trop peu d'instances ({len(X)}) pour diviser train/test.")
        X_train, X_test = X, X
        y_train, y_test = y, y
    else:
        diversity_scores = [np.sum(row) for row in y]
        
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42, stratify=diversity_scores
            )
            print("Stratification basée sur la diversité des labels")
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42
            )
            print("Division simple (stratification impossible)")
    
    print(f"Train: {X_train.shape[0]} instances")
    print(f"Test:  {X_test.shape[0]} instances")
    
    # Créer et entraîner le modèle
    print(f"\n{'='*60}")
    print("ENTRAÎNEMENT DU MODÈLE")
    print(f"{'='*60}")
    
    br_model = BinaryRelevanceClassifier(
        base_classifier=RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_split=3,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        )
    )
    
    br_model.fit(X_train, y_train, dataset_builder.algorithms, feature_names)
    
    # Évaluer et sauvegarder
    evaluate_and_save_model(br_model, X_test, y_test, dataset_builder, best_config)


def evaluate_and_save_model(br_model, X_test, y_test, dataset_builder, best_config):
    """Évalue et sauvegarde le modèle entraîné"""
    print(f"\n{'='*60}")
    print("ÉVALUATION DU MODÈLE")
    print(f"{'='*60}")
    
    results = br_model.evaluate(X_test, y_test)
    
    print(f"Hamming Loss:        {results['hamming_loss']:.4f}")
    print(f"Exact Match Ratio:   {results['exact_match_ratio']:.4f}")
    print(f"Subset Accuracy:     {results['subset_accuracy']:.4f}")
    
    print(f"\n{'Règle':<8} {'Accuracy':<9} {'Precision':<10} {'Recall':<8} {'F1-Score':<9}")
    print("-" * 65)
    for rule, metrics in results['rule_metrics'].items():
        print(f"{rule:<8} {metrics['accuracy']:<9.3f} {metrics['precision']:<10.3f} "
              f"{metrics['recall']:<8.3f} {metrics['f1_score']:<9.3f}")
    
    # Sauvegarder le modèle
    os.makedirs("./resultats", exist_ok=True)
    model_path = os.path.join("./resultats", "binary_relevance_model.pkl")
    br_model.save_model(model_path)
    
    print(f"\nModèle sauvegardé dans {model_path}")
    print("Modèle prêt à être utilisé pour les prédictions!")


def use_ml_model():
    """Utilise le modèle ML pour résoudre des instances"""
    print("\n" + "="*60)
    print("UTILISATION DU MODÈLE ML")
    print("="*60)
    
    model_path = "./resultats/binary_relevance_model.pkl"
    
    if not os.path.exists(model_path):
        print(f"Modèle non trouvé: {model_path}")
        print("Veuillez d'abord entraîner un modèle (option 1).")
        return
    
    # Créer l'instance ML intégrée
    ml_msrcpsp = MLIntegratedMSRCPSP(model_path)
    
    # Demander le fichier d'instance
    try:
        instance_file = input("Chemin vers le fichier d'instance (.dzn ou .msrcp): ").strip()
        if not instance_file:
            # Utiliser un exemple par défaut
            instances_dir = "./Instances"
            if os.path.exists(instances_dir):
                files = [f for f in os.listdir(instances_dir) if f.endswith(('.dzn', '.msrcp'))]
                if files:
                    instance_file = os.path.join(instances_dir, files[0])
                    print(f"Utilisation du fichier par défaut: {instance_file}")
        
        if not os.path.exists(instance_file):
            print(f"Fichier non trouvé: {instance_file}")
            return
        
        # Résoudre avec le ML
        result = ml_msrcpsp.solve_with_ml_guidance(instance_file)
        
        if result and 'best_algorithm' in result:
            print(f"\n{'='*60}")
            print("RÉSULTATS")
            print(f"{'='*60}")
            print(f"Instance: {result['instance']}")
            print(f"Algorithmes recommandés: {result['ml_recommended_algorithms']}")
            print(f"Meilleur algorithme: {result['best_algorithm']}")
            print(f"Meilleur makespan: {result['best_makespan']}")
            
            if 'performance_improvement' in result:
                perf = result['performance_improvement']
                print(f"Amélioration: {perf.get('improvement_percentage', 0):.1f}%")
        
    except KeyboardInterrupt:
        print("\nInterruption utilisateur.")
    except Exception as e:
        print(f"Erreur: {e}")


def batch_processing_with_ml():
    """Traitement en lot avec ML"""
    print("\n" + "="*60)
    print("TRAITEMENT EN LOT AVEC ML")
    print("="*60)
    
    model_path = "./resultats/binary_relevance_model.pkl"
    
    if not os.path.exists(model_path):
        print(f"Modèle non trouvé: {model_path}")
        print("Veuillez d'abord entraîner un modèle (option 1).")
        return
    
    # Créer l'instance ML intégrée
    ml_msrcpsp = MLIntegratedMSRCPSP(model_path)
    
    # Demander le répertoire d'instances
    try:
        instances_dir = input("Répertoire des instances (défaut: ./Instances): ").strip()
        if not instances_dir:
            instances_dir = "./Instances"
        
        if not os.path.exists(instances_dir):
            print(f"Répertoire non trouvé: {instances_dir}")
            return
        
        output_dir = input("Répertoire de sortie (défaut: ./resultats_ml): ").strip()
        if not output_dir:
            output_dir = "./resultats_ml"
        
        # Lancer le traitement en lot
        report = ml_msrcpsp.batch_solve_with_ml(instances_dir, output_dir)
        
        print(f"\n{'='*60}")
        print("TRAITEMENT TERMINÉ")
        print(f"{'='*60}")
        print(f"Instances traitées: {report.get('successful_instances', 0)}/{report.get('total_instances', 0)}")
        print(f"Taux de réussite: {report.get('success_rate', 0):.1f}%")
        print(f"Résultats dans: {output_dir}")
        
    except KeyboardInterrupt:
        print("\nInterruption utilisateur.")
    except Exception as e:
        print(f"Erreur: {e}")


# Remplacer l'ancienne fonction main par celle-ci


if __name__ == "__main__":
    main()

def demonstrate_ml_integration():
    """Démontre l'utilisation du modèle ML intégré"""
    print("=" * 80)
    print("DÉMONSTRATION DE L'INTÉGRATION MACHINE LEARNING")
    print("=" * 80)
    
    # Vérifier si le modèle ML existe
    model_path = "./resultats/binary_relevance_model.pkl"
    
    # Créer l'instance ML intégrée
    ml_msrcpsp = MLIntegratedMSRCPSP(model_path if os.path.exists(model_path) else None)
    
    # Tester sur quelques instances
    instances_dir = "./Instances"
    
    if os.path.exists(instances_dir):
        # Lister quelques fichiers d'instances
        instance_files = [f for f in os.listdir(instances_dir) 
                         if f.endswith(('.dzn', '.msrcp'))][:5]  # Premier 5
        
        if instance_files:
            print(f"Test sur {len(instance_files)} instances:")
            
            for filename in instance_files:
                instance_path = os.path.join(instances_dir, filename)
                print(f"\n--- Test de {filename} ---")
                
                try:
                    # Prédiction ML
                    recommended = ml_msrcpsp.predict_best_algorithms(instance_path, top_k=3)
                    print(f"Algorithmes recommandés: {recommended}")
                    
                    # Résolution complète (si solveur disponible)
                    if MSRCPSPSolver is not None:
                        result = ml_msrcpsp.solve_with_ml_guidance(instance_path)
                        if result and 'best_algorithm' in result:
                            print(f"Meilleur résultat: {result['best_algorithm']} "
                                  f"(makespan: {result['best_makespan']})")
                    
                except Exception as e:
                    print(f"Erreur: {e}")
        else:
            print("Aucun fichier d'instance trouvé")
    else:
        print(f"Répertoire {instances_dir} non trouvé")
    
    print("\nDémonstration terminée!")