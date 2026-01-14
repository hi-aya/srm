# Supplier Risk Management (SRM)

## Présentation générale

Le projet Supplier Risk Management (SRM) a pour objectif de concevoir une plateforme d’aide à la décision permettant d’évaluer, d’expliquer et d’anticiper le risque fournisseur à partir de données métiers. Il s’inscrit dans un contexte industriel où la maîtrise du risque fournisseurs est un levier essentiel de performance, de continuité des opérations et de conformité réglementaire.

Contrairement aux approches classiques basées uniquement sur des indicateurs statiques ou des scores agrégés, le projet SRM repose sur une approche data-driven intégrant des modèles de Machine Learning explicables et des mécanismes d’intelligence artificielle générative afin de proposer, en plus de la prédiction, des recommandations opérationnelles directement exploitables.

---

## Objectifs du projet

Le projet vise à :
- prédire le niveau de risque fournisseur à partir d’indicateurs financiers, logistiques, qualité, réglementaires et ESG ;
- associer à chaque prédiction une probabilité explicite afin de quantifier l’incertitude ;
- expliquer les décisions du modèle à l’aide de méthodes d’Explainable AI (SHAP) afin de garantir la transparence ;
- générer automatiquement des actions correctives structurées, traçables et auditables ;
- stocker l’ensemble des données, prédictions et recommandations afin de permettre un suivi historique et une exploitation future.

---

## Architecture générale

L’architecture du projet est organisée autour de trois couches principales : une interface utilisateur (frontend), une couche applicative (backend) et une couche d’intelligence artificielle, appuyées par une base de données centralisée.

Le frontend permet à l’utilisateur de saisir les données fournisseur et de visualiser les résultats. Le backend assure la logique métier, l’appel aux modèles, le calcul des explications et l’orchestration du module de génération d’actions. La couche IA regroupe le modèle de classification, le calcul SHAP et le module RAG couplé à un LLM. L’ensemble des résultats est persisté dans une base Supabase afin d’assurer la traçabilité.

---

## Approche intelligence artificielle

La prédiction du risque fournisseur repose sur un modèle de Machine Learning supervisé entraîné à partir d’un ensemble de variables représentant les principales dimensions du risque. Le modèle fournit une classe de risque ainsi qu’une probabilité associée.

Afin de rendre les résultats interprétables, le projet intègre une explicabilité locale basée sur SHAP. Pour chaque prédiction, les variables les plus contributives sont identifiées, leur sens d’impact est précisé et leur contribution relative est quantifiée. Ces informations constituent un élément central de justification de la décision.

Les résultats de la classification et de l’explicabilité sont ensuite exploités par un module RAG (Retrieval-Augmented Generation). Ce module sélectionne automatiquement des contenus issus de playbooks internes en fonction du niveau de risque et des variables dominantes, puis sollicite un modèle de langage de manière strictement encadrée afin de générer des actions correctives. Les sorties sont produites sous un format structuré et auditable, incluant notamment la justification, la variable cible, le responsable, les indicateurs de suivi et les délais.

---

## Structure du dépôt

Le dépôt est structuré de manière modulaire afin de séparer clairement les responsabilités techniques :

