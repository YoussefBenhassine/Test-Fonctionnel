"""
CategoryPage : Page de catégorie de produits
Gère la navigation et la vérification des pages de catégorie
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CategoryPage(BasePage):
    """Page de catégorie de produits"""
    
    # Sélecteurs pour les éléments de la page catégorie
    CATEGORY_TITLE = (By.XPATH, "//h1 | //h2[contains(@class, 'category')] | //div[contains(@class, 'category-title')]")
    PRODUCTS_LIST = (By.XPATH, "//div[contains(@class, 'products')] | //ul[contains(@class, 'products')] | //div[contains(@class, 'product-list')]")
    PRODUCT_ITEMS = (By.XPATH, "//div[contains(@class, 'product')] | //article[contains(@class, 'product')] | //li[contains(@class, 'product')]")
    BREADCRUMB = (By.XPATH, "//nav[contains(@class, 'breadcrumb')] | //ol[contains(@class, 'breadcrumb')] | //div[contains(@class, 'breadcrumb')]")
    
    def __init__(self, driver):
        
        super().__init__(driver)
    
    def verify_category_page_loaded(self):
        
        import time
        time.sleep(2)  # Attendre le chargement de la page
        
        # Vérifier la présence d'éléments caractéristiques d'une page catégorie
        # 1. Vérifier la présence de produits ou de la liste de produits
        products_present = self.is_element_present(*self.PRODUCTS_LIST, timeout=5) or \
                          self.is_element_present(*self.PRODUCT_ITEMS, timeout=5)
        
        # 2. Vérifier la présence d'un titre de catégorie ou breadcrumb
        title_present = self.is_element_present(*self.CATEGORY_TITLE, timeout=3)
        breadcrumb_present = self.is_element_present(*self.BREADCRUMB, timeout=3)
        
        # 3. Vérifier que l'URL contient des indices de catégorie
        current_url = self.get_current_url().lower()
        url_indicators = ['categorie', 'category', 'produit', 'product', 'informatique', 'telephonie']
        url_valid = any(indicator in current_url for indicator in url_indicators)
        
        # La page est valide si au moins un de ces éléments est présent
        return products_present or title_present or breadcrumb_present or url_valid
    
    def get_category_name(self):
        
        try:
            if self.is_element_present(*self.CATEGORY_TITLE, timeout=3):
                return self.get_text(*self.CATEGORY_TITLE)
        except:
            pass
        return None

