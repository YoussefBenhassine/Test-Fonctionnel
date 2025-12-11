# Projet d'Automatisation de Tests - Tunisianet

Ce projet automatise les tests fonctionnels du site e-commerce Tunisianet en utilisant Selenium et Python.

## 📋 Description

Le projet implémente un test end-to-end complet qui couvre :
- ✅ Navigation vers la page d'accueil
- ✅ Recherche de produits
- ✅ Sélection d'un produit
- ✅ Ajout au panier
- ✅ Vérification du panier
- ✅ Début du processus de checkout

## 🛠️ Technologies utilisées

- **Python 3** : Langage de programmation
- **Selenium WebDriver** : Automatisation du navigateur
- **pytest** : Framework de test
- **Webdriver Manager** : Gestion automatique des drivers Chrome
- **Page Object Model (POM)** : Architecture de test maintenable

## 📁 Structure du projet

```
amazon_test_project/
│── tests/
│   └── test_tunisianet_flow.py      # Test end-to-end principal
│── pages/
│   ├── base_page.py                  # Classe de base avec actions génériques
│   ├── home_page.py                  # Page d'accueil et recherche
│   ├── results_page.py               # Page des résultats de recherche
│   ├── product_page.py               # Page de détail produit
│   └── cart_page.py                  # Page du panier
│── utils/
│   └── driver_factory.py             # Factory pour créer le WebDriver
│── requirements.txt                  # Dépendances Python
│── README.md                         # Documentation
```

## 🚀 Installation

### Prérequis

- Python 3.7 ou supérieur
- Chrome browser installé sur votre machine

### Étapes d'installation

1. **Cloner ou télécharger le projet**

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - Sur Windows :
     ```bash
     venv\Scripts\activate
     ```
   - Sur Linux/Mac :
     ```bash
     source venv/bin/activate
     ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Exécution des tests

### Exécuter tous les tests
```bash
pytest -s -v
```

### Exécuter un test spécifique
```bash
pytest tests/test_tunisianet_flow.py -s -v
```

### Options utiles
- `-s` : Affiche les print statements
- `-v` : Mode verbeux (affiche plus de détails)
- `--headed` : Exécute les tests en mode visible (par défaut)
- `--html=report.html` : Génère un rapport HTML (nécessite pytest-html)

## 📝 Architecture

### Page Object Model (POM)

Le projet utilise le pattern Page Object Model pour une meilleure maintenabilité :

- **BasePage** : Contient toutes les actions génériques (click, send_keys, wait, etc.)
- **HomePage** : Gère la navigation et la recherche
- **ResultsPage** : Gère la sélection de produits dans les résultats
- **ProductPage** : Gère l'ajout au panier
- **CartPage** : Gère la vérification du panier et le checkout

### Driver Factory

Le `driver_factory.py` configure automatiquement Chrome WebDriver avec :
- Webdriver Manager pour télécharger automatiquement le driver
- Fenêtre maximisée
- Implicit wait de 10 secondes
- Options Chrome optimisées

## 🔍 Fonctionnalités testées

Le test `test_full_tunisianet_flow` vérifie :

1. **Navigation** : Accès à la page d'accueil et vérification du chargement
2. **Recherche** : Recherche d'un produit (ex: "laptop") et vérification des résultats
3. **Sélection** : Clic sur le premier produit dans les résultats
4. **Ajout au panier** : Ajout du produit au panier
5. **Vérification panier** : Confirmation que le produit est bien dans le panier
6. **Checkout** : Début du processus de commande (redirection vers checkout)

## ⚙️ Configuration

### Modifier le produit recherché

Dans `tests/test_tunisianet_flow.py`, ligne avec `search_term` :
```python
search_term = "laptop"  # Modifier ici
```

### Mode headless (sans interface graphique)

Dans `utils/driver_factory.py`, décommenter la ligne :
```python
chrome_options.add_argument("--headless")
```

## 🐛 Dépannage

### Le driver ne se télécharge pas
- Vérifiez votre connexion internet
- Webdriver Manager télécharge automatiquement le driver compatible

### Les sélecteurs ne fonctionnent pas
- Le site peut avoir changé sa structure HTML
- Vérifiez les sélecteurs dans les fichiers `pages/*.py`
- Utilisez les outils de développement du navigateur pour inspecter les éléments

### Timeout errors
- Augmentez les timeouts dans `base_page.py` (WebDriverWait)
- Vérifiez votre connexion internet

## 📚 Ressources

- [Documentation Selenium](https://www.selenium.dev/documentation/)
- [Documentation pytest](https://docs.pytest.org/)
- [Webdriver Manager](https://github.com/SergeyPirogov/webdriver_manager)

## 👤 Auteur

Projet créé pour l'automatisation des tests du site Tunisianet.

## 📄 Licence

Ce projet est à des fins éducatives et de test.
