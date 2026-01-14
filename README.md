# Supplier Risk Management System (SRMS)

## 1. Présentation générale

Le **Supplier Risk Management System (SRMS)** est une plateforme d’aide à la décision destinée à l’évaluation, l’explication et le pilotage du risque fournisseur.  
Le système s’appuie sur des techniques de **Machine Learning**, d’**explicabilité des modèles (SHAP)** et d’**Intelligence Artificielle Générative (RAG)** afin de transformer des données de performance fournisseur en **indicateurs de risque compréhensibles** et en **actions correctives opérationnelles**.

Le projet adopte une approche orientée industrie et management, avec une architecture claire, modulaire et extensible.

---

## 2. Objectifs du projet

- Évaluer le niveau de risque fournisseur à partir de données multi-critères.
- Expliquer les décisions du modèle grâce à l’explicabilité SHAP.
- Générer automatiquement des recommandations et plans d’actions correctifs via un module RAG.
- Centraliser les données et résultats dans une base PostgreSQL (Supabase).
- Proposer une interface web claire facilitant la prise de décision managériale.

---

## 3. Architecture globale

Le système repose sur une architecture **frontend / backend découplée**.

### 3.1 Frontend
- Framework : Next.js (App Router)
- Interface utilisateur : Tailwind CSS / composants UI
- Fonctions principales :
  - Saisie des métriques fournisseur
  - Sélection d’un fournisseur réel
  - Visualisation du risque et de sa probabilité
  - Affichage des facteurs explicatifs SHAP
  - Consultation des actions correctives générées par le LLM

### 3.2 Backend
- Framework : FastAPI
- Fonctions principales :
  - Exposition d’API REST
  - Chargement et exécution du modèle de Machine Learning
  - Calcul des probabilités de risque
  - Génération des explications SHAP
  - Appel du module RAG pour la génération d’actions

### 3.3 Base de données
- SGBD : PostgreSQL (Supabase)
- Rôle :
  - Stockage des fournisseurs
  - Historisation des métriques de performance
  - Sauvegarde des analyses de risque et des recommandations

---

## 4. Modélisation des données

### 4.1 Table `suppliers`
Contient les données maîtres des fournisseurs (données stables).

Exemples de champs :
- id (UUID)
- name
- country
- sector
- supplier_type
- criticality_level
- created_at

### 4.2 Table `supplier_metrics`
Contient les données quantitatives utilisées par le modèle (données temporelles).

Exemples de champs :
- supplier_id (clé étrangère)
- year
- financial_stability_score
- delivery_performance_score
- quality_compliance_score
- regulatory_adherence_score
- sustainability_score
- past_risk_level
- erp_transactions
- incidents_count
- mcdm_score

### 4.3 Table `risk_analysis`
Contient les résultats issus de l’analyse IA.

Exemples de champs :
- supplier_id (clé étrangère)
- risk_class
- risk_probability
- shap_json
- llm_actions
- created_at

---

## 5. Machine Learning et explicabilité

### 5.1 Modèle de risque
- Type : classificateur supervisé
- Entrées : métriques de performance fournisseur
- Sorties :
  - Classe de risque (High / Medium / Low)
  - Probabilité associée

### 5.2 Explicabilité SHAP
- Méthode : SHAP TreeExplainer
- Résultats :
  - Contribution de chaque variable à la prédiction
  - Identification des facteurs dominants du risque
- Objectif :
  - Transparence des décisions du modèle
  - Compréhension managériale des résultats

---

## 6. Module RAG (LLM)

Le module RAG exploite les résultats de l’analyse (classe de risque, probabilité et facteurs SHAP) pour générer des **actions correctives contextualisées**.

Chaque action générée inclut :
- Description de l’action
- Type (immédiate, court terme, moyen terme)
- Responsable (owner)
- KPI associé
- Livrable attendu
- Délai de mise en œuvre
- Condition de déclenchement
- Justification basée sur les facteurs de risque

Ce module permet de transformer une analyse prédictive en un véritable outil de pilotage opérationnel.

---

## 7. Parcours utilisateur

1. Sélection d’un fournisseur existant
2. Saisie des métriques de performance
3. Lancement de l’analyse de risque
4. Visualisation des résultats :
   - Classe de risque
   - Probabilité
   - Facteurs explicatifs SHAP
5. Consultation des actions correctives recommandées

---

## 8. Points forts du projet

- Architecture claire et modulaire
- Intégration de l’explicabilité au cœur de la décision
- Génération automatique d’actions exploitables
- Historisation des analyses
- Approche réaliste et industrialisable

---

## 9. Perspectives d’amélioration

- Analyse multi-années
- Comparaison et classement de fournisseurs
- Suivi de l’exécution des actions correctives
- Tableau de bord global du portefeuille fournisseurs
- Export des résultats (PDF, Excel)
- Gestion des droits et rôles utilisateurs

---

## 10. Auteur

Projet réalisé dans un cadre académique en génie industriel et data science, orienté gestion du risque fournisseur et aide à la décision dans un contexte industriel.
