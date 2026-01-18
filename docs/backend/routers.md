# Backend – Routers (API Layer)

Ce document décrit la **couche Routers du backend** de la plateforme **Supplier Risk Management (SRM)**.  
Les routers constituent la **porte d’entrée API** du système et assurent l’orchestration entre le **frontend**, les **services métier** et la **base de données**, tout en respectant une séparation stricte des responsabilités.

---

## 1. Rôle de la couche Routers

La couche `routers` est responsable de :
- l’exposition des **endpoints REST**
- la validation des entrées via **Pydantic**
- l’orchestration des services backend
- la gestion des erreurs HTTP
- la normalisation des réponses API

Elle ne contient **aucune logique métier**, celle-ci étant entièrement déléguée à la couche `services`.

---

## 2. Organisation des routers


Chaque router est structuré par **domaine fonctionnel**, facilitant la lisibilité, la maintenance et l’évolutivité.

---

## 3. Risk Router – Analyse du risque fournisseur

**Fichier :** `app/routers/risk.py`

### Endpoint


### Objectif

Analyser le risque d’un fournisseur à partir de métriques métier en combinant :
- prédiction Machine Learning
- explicabilité SHAP
- génération optionnelle d’actions correctives via LLM (RAG)

---

### Paramètres

**Body (JSON – `RiskRequest`)**  
Contient l’ensemble des indicateurs nécessaires à l’évaluation du risque fournisseur.

**Query parameter**
- `with_llm` (bool, optionnel)  
  - `false` : prédiction + explicabilité uniquement  
  - `true` : prédiction + explicabilité + actions correctives IA  

---

### Flux de traitement

1. Réception et validation du payload via Pydantic  
2. Conversion du modèle Pydantic en dictionnaire Python  
3. Appel du `RiskModelService`  
4. Exécution du pipeline décisionnel :
   - prédiction du risque
   - calcul SHAP
   - génération RAG (si activée)
   - persistance des résultats
5. Retour d’une réponse JSON structurée au frontend

---

### Gestion des erreurs

- Capture globale des exceptions
- Journalisation côté backend
- Retour d’une erreur `HTTP 500` avec message explicite

Cette gestion garantit la **robustesse** et la **traçabilité** des erreurs en environnement réel.

---

## 4. Suppliers Router – Listing des fournisseurs

**Fichier :** `app/routers/suppliers.py`

### Endpoint


### Objectif

Fournir au frontend la liste des fournisseurs **valides** pour :
- la sélection utilisateur
- l’analyse du risque
- le reporting

---

### Logique appliquée

- Connexion à Supabase via le client centralisé
- Sélection restreinte des champs :
  - `uuid`
  - `name`
  - `country`
- Exclusion explicite des entrées techniques ou invalides

Cette approche permet :
- de limiter l’exposition des données
- d’améliorer la qualité des données côté frontend
- de sécuriser l’API

---

### Gestion des erreurs

- Supabase non initialisé → `HTTP 500`
- Erreur d’exécution → `HTTP 500`
- Journalisation systématique des exceptions

---

## 5. Bonnes pratiques mises en œuvre

- Séparation stricte **Routers / Services**
- Validation systématique des entrées
- Endpoints REST clairs et cohérents
- Gestion centralisée des erreurs
- Architecture prête pour le versioning et la montée en charge

---

## 6. Rôle dans l’architecture globale

Les routers assurent l’interface entre :
- le **frontend** (saisie, affichage, actions)
- le **moteur décisionnel IA**
- la **base de données**

Ils constituent ainsi le **point de jonction critique** entre l’UX et la logique métier.

---

## 7. Conclusion

La couche Routers du backend SRM fournit une **API robuste, lisible et orientée métier**, garantissant :
- une intégration fluide avec le frontend
- une orchestration fiable des services IA
- une gouvernance claire des flux de données

Cette conception est alignée avec les **standards industriels** attendus pour une plateforme décisionnelle basée sur l’intelligence artificielle.
