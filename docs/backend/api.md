### Rôle
Ce répertoire contient les **points d’entrée de l’API REST**.  
Il expose les routes accessibles par le frontend ou des services externes.

### Contenu typique
- Définition des routes HTTP (POST, GET)
- Validation des requêtes via des schémas
- Gestion des paramètres (query, body)
- Gestion des erreurs HTTP

### Exemple fonctionnel
- `/risk/analyze` :
  - Reçoit les métriques fournisseur
  - Déclenche l’analyse de risque
  - Retourne la classe de risque, la probabilité, SHAP et les actions RAG

### Responsabilités
- Orchestration des appels aux services
- Aucune logique métier complexe
- Aucun calcul ML direct
