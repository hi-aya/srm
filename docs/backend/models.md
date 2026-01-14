## 2.3 `backend/models/`

### Rôle général

Le répertoire `backend/models/` contient l’ensemble des **artefacts de Machine Learning** utilisés par le système SRMS.  
Il permet de **séparer clairement le code applicatif** des **modèles entraînés**, facilitant ainsi la maintenance, le versionnage et l’évolution des algorithmes.

Aucune logique métier ou API n’est implémentée dans ce dossier.

---

### Modèle principal : Gradient Boosted Trees (GBT)

Le modèle de prédiction du risque fournisseur repose sur un algorithme de **Gradient Boosted Trees (GBT)**, reconnu pour ses performances élevées sur des données tabulaires hétérogènes.

#### Principe du Gradient Boosting

Le Gradient Boosting est une méthode d’ensemble qui consiste à :
- entraîner une succession d’arbres de décision,
- chaque nouvel arbre corrige les erreurs commises par les précédents,
- l’optimisation est réalisée par descente de gradient sur une fonction de perte.

Le modèle final est une **combinaison pondérée de plusieurs arbres faibles**, produisant une prédiction robuste et non linéaire.

---

### Justification du choix du GBT

Le GBT a été retenu pour les raisons suivantes :

- Excellente performance sur des données structurées multi-critères
- Capacité à modéliser des relations non linéaires complexes
- Robustesse face aux variables corrélées
- Compatibilité native avec les méthodes d’explicabilité SHAP
- Adapté à un contexte industriel et décisionnel

Ce choix est particulièrement pertinent pour l’analyse du risque fournisseur, où les interactions entre critères sont complexes et non linéaires.

---

### Entrées du modèle

Le modèle GBT exploite un vecteur de caractéristiques quantitatives, notamment :

- Financial_Stability_Score  
- Delivery_Performance_Score  
- Quality_Compliance_Score  
- Regulatory_Adherence_Score  
- Sustainability_Score  
- Past_Risk_Level  
- ERP_Transactions  
- Incidents_Count  
- MCDM_Score  

Ces variables représentent une vision multi-dimensionnelle de la performance fournisseur.

---

### Sorties du modèle

Le modèle produit :

- une **classe de risque** (par exemple : High / Medium / Low),
- une **probabilité associée** à la classe prédite.

Ces sorties constituent la base des modules d’explicabilité et de génération d’actions.

---

### Stockage du modèle

Le modèle entraîné est sérialisé et stocké sous forme de fichier :

- `risk_classifier.joblib`

Ce format permet :
- un chargement rapide en mémoire,
- une intégration directe dans les services backend,
- une séparation claire entre entraînement et inférence.

---

### Intégration avec SHAP

Le choix du GBT permet une intégration directe avec **SHAP TreeExplainer**, offrant :

- une explication locale de chaque prédiction,
- la contribution exacte de chaque variable,
- une transparence totale des décisions du modèle.

Ces explications sont exploitées à la fois :
- pour l’affichage frontend,
- comme contexte d’entrée du module RAG.

---

### Évolutivité

Le répertoire `models/` est conçu pour permettre :
- le remplacement du modèle sans modification du frontend,
- la comparaison de plusieurs modèles (ex. Random Forest, XGBoost),
- l’intégration future de modèles temporels ou hybrides.

---
