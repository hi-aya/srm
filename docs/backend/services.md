# Backend – Services Layer

Ce document décrit la **couche Services du backend** de la plateforme **Supplier Risk Management (SRM)**.  
Cette couche encapsule toute la **logique métier critique**, indépendamment des routes API, afin de garantir une architecture **modulaire, maintenable, testable et auditable**.

---

## 1. Rôle de la couche Services

La couche `services` est responsable de :
- l’exécution du **modèle de Machine Learning**
- l’**explicabilité des décisions** (SHAP)
- la **génération d’actions correctives par IA (LLM + RAG)**
- la **persistance et traçabilité** des résultats

Elle constitue le **cœur décisionnel** du backend SRM.

---

## 2. Architecture des services


Chaque service respecte le principe de **responsabilité unique (SRP)**.

---

## 3. RiskModelService – Prédiction & explicabilité

**Fichier :** `app/services/risk_model.py`

### Objectif
Le `RiskModelService` assure :
- la prédiction du niveau de risque fournisseur
- le calcul de la probabilité associée
- l’explication locale des décisions via SHAP
- l’appel optionnel au service LLM
- la sauvegarde complète des résultats pour audit

### Modèle utilisé
- Type : `RandomForestClassifier`
- Fichier : `models/risk_classifier.joblib`

**Justification :**
- excellente performance sur données tabulaires
- robustesse aux relations non linéaires
- compatibilité native avec SHAP (`TreeExplainer`)

### Variables d’entrée
Le modèle exploite les indicateurs suivants :
- `Financial_Stability_Score`
- `Delivery_Performance_Score`
- `Quality_Compliance_Score`
- `Regulatory_Adherence_Score`
- `Sustainability_Score`
- `Past_Risk_Level`
- `ERP_Transactions`
- `Incidents_Count`
- `MCDM_Score`

Ces variables couvrent les dimensions **financières, qualité, supply chain, réglementaires et stratégiques** du risque fournisseur.

### Pipeline de traitement
1. Construction du vecteur d’entrée
2. Prédiction de la classe de risque
3. Calcul de la probabilité associée
4. Calcul des valeurs SHAP locales
5. Identification des facteurs dominants
6. Génération optionnelle d’actions IA
7. Stockage des résultats dans la base

### Explicabilité SHAP
Pour chaque fournisseur, le service fournit :
- la valeur réelle de chaque feature
- la contribution SHAP
- le sens d’impact (augmentation / réduction du risque)
- la contribution relative (%)

Cette approche garantit **transparence, traçabilité et acceptabilité métier**.

---

## 4. LLM RAG Service – Actions correctives

**Fichier :** `app/services/llm_rag.py`

### Objectif
Transformer une prédiction explicable en **plan d’actions correctives opérationnel**, structuré et auditable.

### Approche RAG
Le service applique une stratégie **Retrieval-Augmented Generation** :
1. Sélection d’un playbook interne selon la classe de risque
2. Extraction ciblée des passages pertinents
3. Injection du contexte dans le prompt
4. Génération d’actions strictement contrôlées

### Gouvernance IA
Le prompt impose :
- sortie uniquement en JSON valide
- aucune hallucination
- actions liées à des features réelles
- justification basée sur valeur + SHAP + contribution
- délais cohérents avec le type d’action

### Résultat
Le service retourne :
- un résumé du risque
- les principaux drivers explicatifs
- 6 à 10 actions correctives avec :
  - responsable métier
  - KPI
  - seuil de succès
  - livrable
  - fréquence
  - délai

Ces actions sont directement exploitables par les équipes opérationnelles.

---

## 5. Supabase Client – Persistance & audit

**Fichier :** `app/services/supabase_client.py`

### Rôle
Fournir une interface centralisée et sécurisée vers Supabase pour :
- stocker les prédictions
- historiser les explications SHAP
- conserver les actions générées par IA

### Sécurité et robustesse
- utilisation du **Service Role Key**
- connexion conditionnelle via variables d’environnement
- fonctionnement dégradé si Supabase indisponible

---

## 6. Traçabilité et auditabilité

Chaque prédiction sauvegardée inclut :
- données d’entrée
- résultat du modèle
- explication SHAP
- actions correctives IA

Cela permet :
- audits internes
- analyses longitudinales
- amélioration continue des modèles

---

## 7. Conclusion

La couche Services du backend SRM met en œuvre une **chaîne décisionnelle complète**, de la donnée brute à l’action corrective.  
Elle combine **Machine Learning**, **explicabilité**, **IA générative contrôlée** et **gouvernance du risque**, répondant aux exigences d’un **système industriel réel**.
