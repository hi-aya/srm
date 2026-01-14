# Frontend – Interface utilisateur

## Objectif du frontend

Le frontend du projet SRM a pour objectif de fournir une interface claire et structurée permettant aux utilisateurs de saisir les données fournisseur, de lancer une analyse de risque et de visualiser les résultats produits par le système.

Il constitue le point de contact principal entre l’utilisateur et les capacités d’analyse du backend.

---

## Rôle fonctionnel

Le frontend permet :
- la saisie ou la modification des indicateurs fournisseur ;
- le déclenchement de l’analyse de risque ;
- l’affichage de la classe de risque et de la probabilité associée ;
- la visualisation des facteurs explicatifs ;
- la consultation des actions correctives proposées.

L’interface est conçue pour guider l’utilisateur tout au long du processus d’analyse.

---

## Parcours utilisateur

Le parcours utilisateur est structuré en plusieurs étapes logiques :

1. Accès à la page d’analyse.
2. Saisie des indicateurs fournisseur.
3. Lancement de l’analyse.
4. Consultation des résultats de classification.
5. Analyse des facteurs explicatifs.
6. Lecture des actions correctives recommandées.

Chaque étape correspond à un état clair du système et limite les ambiguïtés pour l’utilisateur.

---

## Interaction avec le backend

Le frontend communique avec le backend via des appels API. Les données sont transmises sous forme de structures JSON et les résultats sont affichés sans transformation métier côté client.

Cette approche garantit que :
- la logique métier reste centralisée ;
- le frontend demeure léger et maintenable ;
- les résultats affichés correspondent exactement aux décisions calculées.

---

## Présentation des résultats

Les résultats sont présentés de manière structurée :
- le niveau de risque est affiché de façon explicite ;
- les facteurs explicatifs sont ordonnés par importance ;
- les actions correctives sont listées avec leurs caractéristiques principales.

L’objectif n’est pas seulement d’informer, mais de faciliter la prise de décision.

---

## Rôle du frontend dans le projet

Le frontend joue un rôle essentiel dans l’adoption du système SRM. En rendant les résultats compréhensibles et exploitables, il permet de transformer une analyse algorithmique complexe en un outil d’aide à la décision utilisable en contexte industriel.
