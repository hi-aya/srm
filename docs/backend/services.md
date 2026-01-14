### Rôle
Cœur fonctionnel du backend.  
Ce répertoire contient toute la **logique métier**, **Machine Learning**, **explicabilité** et **RAG**.

### Sous-composants clés

#### `risk_model.py`
- Chargement du modèle de Machine Learning (joblib)
- Préparation des features
- Prédiction du risque
- Calcul des probabilités
- Génération des explications SHAP
- Structuration du résultat final

#### `llm_rag.py`
- Génération des actions correctives
- Exploitation des résultats ML + SHAP
- Production de recommandations contextualisées
- Transformation de l’analyse en décisions opérationnelles

#### `supabase_client.py`
- Connexion sécurisée à Supabase
- Insertion des analyses
- Historisation des résultats
- Gestion des erreurs de persistance

### Responsabilités
- Implémentation complète de la logique métier
- Indépendance vis-à-vis de l’API
- Réutilisabilité et testabilité
