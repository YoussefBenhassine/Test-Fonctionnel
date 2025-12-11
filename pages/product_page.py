"""
ProductPage : Page de détail d'un produit
Gère l'ajout du produit au panier
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Page de détail d'un produit"""
    
    # Sélecteurs pour le bouton d'ajout au panier
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(text(), 'Ajouter') or contains(text(), 'Panier') or contains(text(), 'Acheter')] | //a[contains(text(), 'Ajouter') or contains(text(), 'Panier')]")
    ADD_TO_CART_BUTTON_ALT = (By.XPATH, "//button[contains(@class, 'add-to-cart') or contains(@class, 'cart')] | //a[contains(@class, 'add-to-cart')]")
    PRODUCT_TITLE = (By.XPATH, "//h1 | //h2[contains(@class, 'product')] | //div[contains(@class, 'product-title')]")
    CART_ICON = (By.XPATH, "//a[contains(@href, 'cart') or contains(@href, 'panier')] | //i[contains(@class, 'cart')]/parent::a")
    
    def __init__(self, driver):
        
        super().__init__(driver)
    
    def add_to_cart(self):
        
        # Attendre que la page se charge
        import time
        time.sleep(2)
        
        # Essayer plusieurs sélecteurs pour le bouton d'ajout au panier
        add_button_selectors = [
            (By.XPATH, "//button[contains(text(), 'Ajouter au panier') or contains(text(), 'Ajouter')]"),
            (By.XPATH, "//button[contains(@class, 'add-to-cart') or contains(@class, 'add_cart')]"),
            (By.XPATH, "//a[contains(text(), 'Ajouter au panier') or contains(text(), 'Ajouter')]"),
            (By.XPATH, "//button[contains(@id, 'add') or contains(@id, 'cart')]"),
            (By.XPATH, "//input[@type='submit' and contains(@value, 'Ajouter')]"),
            (By.XPATH, "//button[contains(@class, 'single_add_to_cart_button')]"),
        ]
        
        button_found = False
        for selector in add_button_selectors:
            try:
                if self.is_element_present(*selector, timeout=3):
                    self.click(*selector)
                    button_found = True
                    # Attendre un peu pour que l'ajout se fasse
                    time.sleep(2)
                    break
            except:
                continue
        
        if not button_found:
            raise Exception("Bouton d'ajout au panier non trouvé")
        
        # Importer CartPage ici pour éviter les imports circulaires
        from pages.cart_page import CartPage
        return CartPage(self.driver)
    
    def go_to_cart(self):
        
        # Essayer de cliquer sur l'icône panier
        cart_selectors = [
            (By.XPATH, "//a[contains(@href, 'cart') or contains(@href, 'panier')]"),
            (By.XPATH, "//i[contains(@class, 'cart')]/parent::a"),
            (By.XPATH, "//span[contains(@class, 'cart')]/parent::a"),
        ]
        
        for selector in cart_selectors:
            try:
                if self.is_element_present(*selector, timeout=3):
                    self.click(*selector)
                    break
            except:
                continue
        
        from pages.cart_page import CartPage
        return CartPage(self.driver)
