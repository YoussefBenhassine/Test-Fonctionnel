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
        import time
        
        # Attendre que le panier se charge complètement
        time.sleep(3)
        
        # Vérifier que nous sommes bien sur la page du panier
        current_url = self.get_current_url().lower()
        if "cart" not in current_url and "panier" not in current_url:
            print(f"[WARNING] URL actuelle ne semble pas être la page du panier: {current_url}")
        
        # 1. Vérifier la présence d'items du panier (méthode principale)
        if self.is_element_present(*self.CART_ITEMS, timeout=10):
            # Vérifier qu'il y a au moins un item avec un nom de produit
            try:
                cart_items = self.find_elements(*self.CART_ITEMS)
                if cart_items and len(cart_items) > 0:
                    print(f"[OK] {len(cart_items)} article(s) trouvé(s) dans le panier")
                    return True
            except:
                pass
        
        # 2. Vérifier qu'il n'y a pas de message "panier vide"
        if self.is_element_present(*self.CART_EMPTY_MESSAGE, timeout=2):
            print("[FAIL] Message 'panier vide' détecté")
            return False
        
        # 3. Vérifier la présence de noms de produits dans le panier
        try:
            product_names = self.find_elements(*self.PRODUCT_IN_CART)
            if product_names and len(product_names) > 0:
                print(f"[OK] {len(product_names)} nom(s) de produit(s) trouvé(s) dans le panier")
                return True
        except:
            pass
        
        # 4. Vérifier l'URL comme dernier recours
        if "cart" in current_url or "panier" in current_url:
            print("[WARNING] Sur la page du panier mais aucun produit détecté")
            return False
        
        print("[FAIL] Aucun produit détecté dans le panier")
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
