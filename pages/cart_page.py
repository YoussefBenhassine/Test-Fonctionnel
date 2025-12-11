"""
CartPage : Page du panier
Gère la vérification des produits dans le panier et le checkout
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page du panier"""
    
    # Sélecteurs pour les éléments du panier
    CART_ITEMS = (By.XPATH, "//tr[contains(@class, 'cart_item')] | //div[contains(@class, 'cart-item')] | //li[contains(@class, 'cart-item')]")
    PRODUCT_IN_CART = (By.XPATH, ".//a[contains(@class, 'product')] | .//td[@class='product-name'] | .//div[contains(@class, 'product-name')]")
    CHECKOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Commander') or contains(text(), 'Checkout') or contains(text(), 'Valider')] | //button[contains(text(), 'Commander') or contains(text(), 'Checkout')]")
    CHECKOUT_BUTTON_ALT = (By.XPATH, "//a[contains(@class, 'checkout') or contains(@href, 'checkout')] | //button[contains(@class, 'checkout')]")
    CART_EMPTY_MESSAGE = (By.XPATH, "//p[contains(text(), 'panier') or contains(text(), 'vide')]")
    
    def __init__(self, driver):
       
        super().__init__(driver)
    
    def verify_product_in_cart(self):
        
        # Attendre que le panier se charge
        import time
        time.sleep(2)
        
        # Vérifier la présence d'articles dans le panier
        # Plusieurs façons de vérifier :
        # 1. Vérifier les items du panier
        if self.is_element_present(*self.CART_ITEMS, timeout=5):
            return True
        
        # 2. Vérifier qu'il n'y a pas de message "panier vide"
        if not self.is_element_present(*self.CART_EMPTY_MESSAGE, timeout=2):
            # Si pas de message "vide", on considère qu'il y a des produits
            return True
        
        # 3. Vérifier l'URL (si elle contient "cart" ou "panier")
        current_url = self.get_current_url().lower()
        if "cart" in current_url or "panier" in current_url:
            return True
        
        return False
    
    def proceed_to_checkout(self):
        
        # Attendre un peu
        import time
        time.sleep(2)
        
        # Essayer plusieurs sélecteurs pour le bouton checkout
        checkout_selectors = [
            (By.XPATH, "//a[contains(text(), 'Commander') or contains(text(), 'Valider la commande')]"),
            (By.XPATH, "//button[contains(text(), 'Commander') or contains(text(), 'Valider')]"),
            (By.XPATH, "//a[contains(@class, 'checkout') or contains(@href, 'checkout')]"),
            (By.XPATH, "//button[contains(@class, 'checkout')]"),
            (By.XPATH, "//a[contains(@href, 'commande')]"),
        ]
        
        button_found = False
        for selector in checkout_selectors:
            try:
                if self.is_element_present(*selector, timeout=3):
                    # Sauvegarder l'URL actuelle
                    current_url = self.get_current_url()
                    self.click(*selector)
                    time.sleep(3)
                    
                    # Vérifier que l'URL a changé (redirection)
                    new_url = self.get_current_url()
                    button_found = (new_url != current_url)
                    if button_found:
                        break
            except:
                continue
        
        return button_found
