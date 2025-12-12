"""
BasePage : Classe de base pour toutes les pages
Contient les actions génériques communes à toutes les pages
Compatible avec Selenium 4.25.0
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Classe de base pour toutes les pages du site"""
    
    def __init__(self, driver):
        """
        Initialise la page avec le driver
        
        Args:
            driver: Instance du WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, by, value):
        """
        Trouve un élément avec WebDriverWait
        
        Args:
            by: Méthode de localisation (By.XPATH, By.ID, etc.)
            value: Valeur du sélecteur
            
        Returns:
            WebElement: L'élément trouvé
        """
        return self.wait.until(EC.presence_of_element_located((by, value)))
    
    def find_elements(self, by, value):
        """
        Trouve plusieurs éléments
        
        Args:
            by: Méthode de localisation
            value: Valeur du sélecteur
            
        Returns:
            List[WebElement]: Liste des éléments trouvés
        """
        return self.driver.find_elements(by, value)
    
    def click(self, by, value):
        
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
    
    def send_keys(self, by, value, text):
        
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, by, value):
       
        element = self.find_element(by, value)
        return element.text
    
    def is_element_present(self, by, value, timeout=5):
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_url_contains(self, text):
        
        self.wait.until(EC.url_contains(text))
    
    def get_current_url(self):
        
        return self.driver.current_url
