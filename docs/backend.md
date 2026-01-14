# Backend – Logique métier et services

## Rôle du backend

Le backend du projet SRM constitue le cœur applicatif du système. Il assure la réception des données, la préparation des entrées pour les modèles d’intelligence artificielle, l’orchestration des différents services (classification, explicabilité, RAG) ainsi que la persistance des résultats.

Il joue également un rôle central dans la traçabilité et la fiabilité des décisions produites par le système.

---

## Organisation générale

Le backend est structuré autour de services spécialisés, chacun ayant une responsabilité bien définie. Cette organisation permet de limiter le couplage et de faciliter la maintenance du code.

Les principaux services sont :
- le service de prédiction du risque fournisseur ;
- le service d’explicabilité SHAP ;
- le service de génération d’actions via RAG ;
- le service d’accès à la base de données Supabase.

---

## Service de prédiction du risque

Le service de prédiction s’appuie sur un modèle de classification préentraîné chargé depuis un fichier de modèle. Les données reçues sont transformées en un format tabulaire conforme aux variables attendues par le modèle.

Le service :
- calcule les probabilités de chaque classe ;
- détermine la classe de risque retenue ;
- extrait la probabilité associée au risque élevé lorsque applicable.

Ce service constitue le point d’entrée principal de l’analyse du risque.

---

## Explicabilité avec SHAP

Une fois la prédiction réalisée, le backend calcule les valeurs SHAP associées à la prédiction courante. Ces valeurs permettent de mesurer l’impact de chaque variable sur la décision finale du modèle.

Le backend sélectionne les facteurs les plus contributifs et enrichit chaque facteur avec :
- la valeur observée ;
- le sens de l’impact sur le risque ;
- la contribution relative en pourcentage.

Ces informations sont ensuite utilisées à des fins d’interprétation et de génération de recommandations.

---

## Génération d’actions correctives (RAG)

Le backend orchestre un module RAG qui combine les résultats de la classification et de l’explicabilité avec des connaissances internes issues de playbooks.

Le processus comprend :
- la sélection du playbook en fonction du niveau de risque ;
- l’extraction ciblée des passages pertinents ;
- la génération d’actions via un modèle de langage strictement contraint.

Les actions produites sont structurées, justifiées et directement exploitables par les équipes métiers.

---

## Persistance des données

Le backend enregistre systématiquement :
- les données d’entrée ;
- les résultats de la prédiction ;
- les explications SHAP ;
- les actions générées par le module RAG.

Cette persistance garantit la traçabilité des décisions et permet un suivi historique du risque fournisseur.

---

## Rôle du backend dans le système global

Le backend assure la cohérence du système SRM en centralisant la logique métier et en garantissant que chaque décision produite est explicable, traçable et reproductible.
