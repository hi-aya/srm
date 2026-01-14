# Architecture du système SRM

## Vue d’ensemble

Le système Supplier Risk Management (SRM) repose sur une architecture modulaire orientée services, conçue pour séparer clairement les responsabilités entre l’interface utilisateur, la logique métier, les traitements d’intelligence artificielle et la persistance des données. Cette séparation permet d’assurer la maintenabilité du système, sa traçabilité ainsi que son évolutivité dans un contexte industriel.

L’architecture suit un schéma client–serveur enrichi par une couche d’intelligence artificielle explicable et un mécanisme de génération de recommandations basé sur des connaissances internes.

---

## Découpage fonctionnel

L’architecture est structurée autour de quatre blocs principaux :

1. Frontend (interface utilisateur)
2. Backend applicatif (API et services)
3. Couche Intelligence Artificielle (classification, SHAP, RAG)
4. Base de données (Supabase)

Les échanges entre ces blocs sont réalisés via des interfaces explicites, principalement sous forme d’API REST et de structures de données JSON.

---

## Flux de données global

Le flux de données du système peut être décrit comme suit :

1. L’utilisateur saisit ou soumet des indicateurs fournisseur via le frontend.
2. Les données sont transmises au backend sous forme de payload structuré.
3. Le backend prépare les données et appelle le service de prédiction du risque.
4. Le modèle de classification calcule la classe de risque et la probabilité associée.
5. Un module d’explicabilité SHAP identifie les facteurs les plus contributifs.
6. Ces résultats sont transmis au module RAG, qui génère des actions correctives.
7. L’ensemble des résultats est stocké dans la base de données.
8. Les résultats sont renvoyés au frontend pour affichage.

---

## Principes de conception

Plusieurs principes ont guidé la conception de l’architecture :

- séparation claire entre calcul, orchestration et présentation ;
- explicabilité systématique des décisions IA ;
- traçabilité complète des entrées et sorties ;
- extensibilité vers d’autres modèles ou sources de données ;
- adaptation à un contexte industriel réel.

---

## Évolutivité

L’architecture permet :
- l’ajout de nouveaux indicateurs fournisseur sans refonte majeure ;
- le remplacement ou l’amélioration du modèle de classification ;
- l’intégration future de données temps réel (ERP, IoT, audits) ;
- l’extension vers des analyses multi-années ou multi-sites.

Cette modularité constitue un élément central du projet SRM.
