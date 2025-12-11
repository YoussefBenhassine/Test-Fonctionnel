"""
Driver Factory pour créer et configurer le WebDriver Chrome
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def _find_chromedriver_exe(driver_dir):
    
    # Chercher récursivement
    for root, dirs, files in os.walk(driver_dir):
        for file in files:
            if file in ['chromedriver.exe', 'chromedriver']:
                path = os.path.join(root, file)
                if os.path.isfile(path):
                    return path
    return None


def get_driver():
    
    # Configuration des options Chrome
    chrome_options = Options()
    # Optionnel : mode headless (décommenter si besoin)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Obtenir le chemin du chromedriver avec Webdriver Manager
    try:
        driver_path = ChromeDriverManager().install()
        
        # Normaliser le chemin (convertir / en \ sur Windows)
        driver_path = os.path.normpath(driver_path)
        
        # Vérifier si le chemin est valide
        if os.path.isfile(driver_path):
            # Si ce n'est pas chromedriver.exe, chercher le bon fichier
            filename = os.path.basename(driver_path)
            if filename not in ['chromedriver.exe', 'chromedriver']:
                # Le répertoire contenant le fichier retourné
                file_dir = os.path.dirname(driver_path)
                
                # Chercher chromedriver.exe dans le même répertoire
                chromedriver_exe = os.path.join(file_dir, 'chromedriver.exe')
                if os.path.isfile(chromedriver_exe):
                    driver_path = chromedriver_exe
                else:
                    # Chercher récursivement dans le répertoire
                    chromedriver_exe = _find_chromedriver_exe(file_dir)
                    if chromedriver_exe:
                        driver_path = chromedriver_exe
                    else:
                        # Chercher dans le répertoire parent
                        parent_dir = os.path.dirname(file_dir)
                        chromedriver_exe = _find_chromedriver_exe(parent_dir)
                        if chromedriver_exe:
                            driver_path = chromedriver_exe
        
        # Normaliser à nouveau après les modifications
        driver_path = os.path.normpath(driver_path)
        
        # Vérifier que le chemin final est valide
        if not os.path.isfile(driver_path):
            raise FileNotFoundError(f"Chromedriver executable non trouve: {driver_path}")
        
        filename = os.path.basename(driver_path)
        if filename not in ['chromedriver.exe', 'chromedriver']:
            raise FileNotFoundError(f"Le chemin ne pointe pas vers chromedriver.exe: {driver_path}")
        
        # Création du service avec le chemin
        service = Service(driver_path)
        
    except Exception as e:
        # En cas d'erreur, essayer sans spécifier le chemin (utilise le PATH système)
        print(f"[WARNING] Erreur avec Webdriver Manager: {e}")
        print("Tentative avec chromedriver du PATH systeme...")
        service = Service()
    
    # Création du driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Configuration du driver
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    return driver
