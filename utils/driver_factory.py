"""
Driver Factory pour créer et configurer le WebDriver Chrome
Compatible avec Selenium 4.25.0
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def _find_chromedriver_exe(driver_dir):
    for root, dirs, files in os.walk(driver_dir):
        for file in files:
            if file in ['chromedriver.exe', 'chromedriver']:
                path = os.path.join(root, file)
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    return path
    return None


def get_driver():
    # Configuration des options Chrome
    chrome_options = Options()
    
    # Arguments essentiels pour la stabilité
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Option pour réduire la détection d'automation
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # Création du service avec Webdriver Manager
    service = None
    try:
        driver_path = ChromeDriverManager().install()
        driver_path = os.path.normpath(driver_path)
        
        # Vérifier si le chemin retourné est directement l'exécutable
        if os.path.isfile(driver_path):
            filename = os.path.basename(driver_path).lower()
            if filename not in ['chromedriver.exe', 'chromedriver']:
                # Le chemin n'est pas l'exécutable, chercher dans le répertoire
                driver_dir = os.path.dirname(driver_path)
                actual_driver = _find_chromedriver_exe(driver_dir)
                if actual_driver:
                    driver_path = actual_driver
                else:
                    # Chercher dans le répertoire parent
                    parent_dir = os.path.dirname(driver_dir)
                    actual_driver = _find_chromedriver_exe(parent_dir)
                    if actual_driver:
                        driver_path = actual_driver
        
        # Vérifier que le chemin final est valide
        if not os.path.isfile(driver_path):
            raise FileNotFoundError(f"Chromedriver executable non trouve: {driver_path}")
        
        service = Service(driver_path)
        
    except Exception as e:
        # En cas d'erreur, utiliser le PATH système
        print(f"[WARNING] Erreur avec Webdriver Manager: {e}")
        print("Tentative avec chromedriver du PATH systeme...")
        service = Service()
    
    # Création du driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Configuration du driver
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    return driver
