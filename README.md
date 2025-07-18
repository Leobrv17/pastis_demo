# Library API

Une API REST moderne pour la gestion d'une bibliothèque, développée avec FastAPI et MongoDB.

## 🚀 Fonctionnalités

### CRUD Complet
- ✅ Créer un livre
- ✅ Lire les informations d'un livre
- ✅ Mettre à jour un livre
- ✅ Supprimer un livre

### Routes Métier
- 📚 **Emprunter un livre** - Système d'emprunt avec date de retour
- 🔄 **Retourner un livre** - Gestion des retours
- 🔍 **Recherche avancée** - Recherche par texte dans titre, auteur, description
- 📊 **Statistiques** - Vue d'ensemble de la bibliothèque

### Fonctionnalités Avancées
- 🔍 Recherche et filtrage (genre, auteur, disponibilité)
- 📄 Pagination optimisée
- 📈 Statistiques temps réel
- 🏷️ Indexation MongoDB pour performances
- 🛡️ Validation stricte des données
- 🐳 Conteneurisation Docker complète

## 🏗️ Architecture

```
app/
├── api/
│   ├── routes/          # Routes FastAPI
│   └── error_handlers.py
├── core/
│   ├── database.py      # Configuration DB
│   └── exceptions.py    # Exceptions métier
├── models/
│   └── book.py          # Modèles Beanie
├── repositories/
│   └── book_repository.py  # Couche d'accès données
├── schemas/
│   └── book.py          # Schémas Pydantic
├── services/
│   └── book_service.py  # Logique métier
├── config.py           # Configuration
└── main.py            # Point d'entrée
```

## 🚀 Démarrage Rapide

### Avec Docker (Recommandé)

```bash
# Cloner le projet
git clone <repository-url>
cd library-api

# Lancer avec Docker Compose
docker-compose up --build
```

L'API sera disponible sur `http://localhost:8000`

### Installation Locale

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env

# Démarrer MongoDB localement
# Puis lancer l'API
uvicorn app.main:app --reload
```

## 📚 Documentation API

Une fois l'application lancée :

- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`
- **OpenAPI JSON** : `http://localhost:8000/openapi.json`

## 🔧 Utilisation

### Créer un livre

```bash
curl -X POST "http://localhost:8000/api/v1/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Le Petit Prince",
    "author": "Antoine de Saint-Exupéry",
    "isbn": "978-2-07-040310-1",
    "publication_year": 1943,
    "genre": "Littérature",
    "pages": 96,
    "description": "Un conte philosophique et poétique"
  }'
```

### Emprunter un livre

```bash
curl -X POST "http://localhost:8000/api/v1/books/{book_id}/borrow" \
  -H "Content-Type: application/json" \
  -d '{
    "borrower_name": "Jean Dupont",
    "days": 14
  }'
```

### Rechercher des livres

```bash
curl "http://localhost:8000/api/v1/books/search/query?q=Prince&limit=5"
```

### Obtenir les statistiques

```bash
curl "http://localhost:8000/api/v1/books/statistics/overview"
```

## 🧪 Tests

```bash
# Installer les dépendances de test
pip install pytest pytest-asyncio httpx

# Lancer les tests
pytest

# Avec couverture
pytest --cov=app tests/
```

## 🔒 Bonnes Pratiques Implémentées

### Code Quality
- **PEP8** : Respect strict des conventions Python
- **Type Hints** : Typage complet pour la lisibilité
- **Fonctions courtes** : Maximum 20-30 lignes par fonction
- **Séparation des responsabilités** : Architecture en couches

### Sécurité
- **Validation stricte** : Pydantic pour tous les inputs
- **Gestion d'erreurs** : Exceptions métier personnalisées
- **Configuration sécurisée** : Variables d'environnement

### Performance
- **Indexation MongoDB** : Optimisation des requêtes
- **Pagination** : Gestion efficace des grandes collections
- **Requêtes asynchrones** : Motor/Beanie pour les performances

### Maintenabilité
- **Architecture modulaire** : Séparation claire des couches
- **Tests** : Structure compatible pytest
- **Documentation** : OpenAPI automatique
- **Conteneurisation** : Déploiement simplifié

## 🛠️ Technologies

- **FastAPI** - Framework web moderne et performant
- **MongoDB** - Base de données NoSQL
- **Beanie** - ODM asynchrone pour MongoDB
- **Pydantic** - Validation et sérialisation des données
- **Motor** - Driver MongoDB asynchrone
- **Docker** - Conteneurisation
- **Pytest** - Framework de tests

## 📝 Configuration

Toutes les configurations sont centralisées dans `app/config.py` et peuvent être surchargées via variables d'environnement :

```python
MONGODB_URL=mongodb://user:password@host:port/database
DATABASE_NAME=library
SECRET_KEY=your-secret-key
DEFAULT_PAGE_SIZE=10
MAX_PAGE_SIZE=100
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT - voir le fichier `LICENSE` pour plus de détails.