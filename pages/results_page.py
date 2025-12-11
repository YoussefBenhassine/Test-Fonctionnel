"""
ResultsPage : Page des résultats de recherche
Gère la sélection d'un produit dans les résultats
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ResultsPage(BasePage):
    
    # Sélecteurs pour les produits
    PRODUCT_ITEMS = (By.XPATH, "//div[contains(@class, 'product')]//a | //article[contains(@class, 'product')]//a | //a[contains(@class, 'product')]")
    PRODUCT_TITLE = (By.XPATH, ".//h2 | .//h3 | .//span[contains(@class, 'title')] | .//div[contains(@class, 'title')]")
    RESULTS_CONTAINER = (By.XPATH, "//div[contains(@class, 'products')] | //div[contains(@class, 'results')] | //ul[contains(@class, 'products')]")
    
    def __init__(self, driver):
        
        super().__init__(driver)
    
    def verify_results_displayed(self):
        
        # Attendre un peu pour que les résultats se chargent
        import time
        time.sleep(2)
        
        # Vérifier la présence de produits
        return self.is_element_present(*self.PRODUCT_ITEMS, timeout=10)
    
    def select_first_product(self):
        
        # Attendre que les produits soient chargés
        import time
        time.sleep(2)
        
        # Trouver tous les liens de produits
        product_selectors = [
            (By.XPATH, "//div[contains(@class, 'product')]//a[contains(@href, '/')]"),
            (By.XPATH, "//article[contains(@class, 'product')]//a[contains(@href, '/')]"),
            (By.XPATH, "//a[contains(@class, 'product') and contains(@href, '/')]"),
            (By.XPATH, "//div[contains(@class, 'product-item')]//a"),
            (By.XPATH, "//a[contains(@href, '/produit') or contains(@href, '/product')]"),
        ]
        
        product_found = False
        for selector in product_selectors:
            try:
                products = self.find_elements(*selector)
                if products and len(products) > 0:
                    # Cliquer sur le premier produit
                    products[0].click()
                    product_found = True
                    break
            except:
                continue
        
        if not product_found:
            raise Exception("Aucun produit trouvé dans les résultats")
        
        # Importer ProductPage ici pour éviter les imports circulaires
        from pages.product_page import ProductPage
        return ProductPage(self.driver)
