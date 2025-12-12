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
    
    # Sélecteurs pour la pop-up de confirmation d'ajout au panier
    CART_SUCCESS_POPUP = (By.XPATH, "//div[contains(text(), 'Produit ajouté au panier') or contains(text(), 'ajouté au panier')] | //div[contains(@class, 'modal') and contains(., 'panier')] | //div[contains(@id, 'cart') and contains(@class, 'modal')]")
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continuer')] | //a[contains(text(), 'Continuer')] | //button[contains(@class, 'continue')] | //a[contains(@class, 'continue')]")
    
    def __init__(self, driver):
        
        super().__init__(driver)
    
    def add_to_cart(self):
        import time
        
        # Attendre que la page se charge
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
                    # Attendre que la pop-up apparaisse
                    time.sleep(3)
                    break
            except:
                continue
        
        if not button_found:
            raise Exception("Bouton d'ajout au panier non trouvé")
        
        # Attendre et cliquer sur le bouton "Continuer" dans la pop-up
        print("[INFO] Recherche de la pop-up de confirmation...")
        continue_button_found = False
        
        # Sélecteurs pour le bouton "Continuer" dans la pop-up
        continue_selectors = [
            (By.XPATH, "//button[contains(text(), 'Continuer')]"),
            (By.XPATH, "//a[contains(text(), 'Continuer')]"),
            (By.XPATH, "//button[contains(@class, 'continue')]"),
            (By.XPATH, "//a[contains(@class, 'continue')]"),
            (By.XPATH, "//div[contains(@class, 'modal')]//button[contains(text(), 'Continuer')]"),
            (By.XPATH, "//div[contains(@class, 'modal')]//a[contains(text(), 'Continuer')]"),
            (By.XPATH, "//div[contains(text(), 'Produit ajouté')]//following::button[contains(text(), 'Continuer')]"),
            (By.XPATH, "//div[contains(text(), 'Produit ajouté')]//following::a[contains(text(), 'Continuer')]"),
        ]
        
        for selector in continue_selectors:
            try:
                if self.is_element_present(*selector, timeout=5):
                    print("[OK] Bouton 'Continuer' trouvé dans la pop-up")
                    self.click(*selector)
                    continue_button_found = True
                    time.sleep(2)  # Attendre que la pop-up se ferme
                    break
            except Exception as e:
                continue
        
        if not continue_button_found:
            print("[WARNING] Bouton 'Continuer' non trouvé, tentative de fermeture de la pop-up...")
            # Essayer de fermer la pop-up avec le bouton X ou en cliquant ailleurs
            try:
                close_button = (By.XPATH, "//button[@class='close'] | //span[contains(@class, 'close')] | //button[contains(@aria-label, 'close')] | //div[contains(@class, 'modal')]//button[contains(@class, 'close')]")
                if self.is_element_present(*close_button, timeout=2):
                    self.click(*close_button)
                    time.sleep(1)
            except:
                pass
        
        # Naviguer vers la page du panier
        print("[INFO] Navigation vers la page du panier...")
        cart_page = self.go_to_cart()
        
        return cart_page
    
    def go_to_cart(self):
        """
        Navigue vers la page du panier en cliquant sur l'icône panier
        """
        import time
        
        # Essayer de cliquer sur l'icône panier
        cart_selectors = [
            (By.XPATH, "//a[contains(@href, 'cart') or contains(@href, 'panier')]"),
            (By.XPATH, "//i[contains(@class, 'cart')]/parent::a"),
            (By.XPATH, "//span[contains(@class, 'cart')]/parent::a"),
            (By.XPATH, "//div[contains(@class, 'cart')]//a"),
            (By.XPATH, "//header//a[contains(@href, 'panier') or contains(@href, 'cart')]"),
        ]
        
        cart_clicked = False
        for selector in cart_selectors:
            try:
                if self.is_element_present(*selector, timeout=5):
                    print("[OK] Icône panier trouvée, clic en cours...")
                    self.click(*selector)
                    cart_clicked = True
                    time.sleep(3)  # Attendre que la page du panier se charge
                    break
            except Exception as e:
                continue
        
        if not cart_clicked:
            # Si on ne trouve pas l'icône, essayer d'accéder directement à l'URL du panier
            print("[WARNING] Icône panier non trouvée, tentative d'accès direct à l'URL...")
            try:
                current_url = self.get_current_url()
                base_url = current_url.split('/')[0] + '//' + current_url.split('/')[2]
                cart_urls = [
                    f"{base_url}/panier",
                    f"{base_url}/cart",
                    f"{base_url}/index.php?controller=cart",
                ]
                for cart_url in cart_urls:
                    try:
                        self.driver.get(cart_url)
                        time.sleep(3)
                        if "cart" in self.get_current_url().lower() or "panier" in self.get_current_url().lower():
                            cart_clicked = True
                            break
                    except:
                        continue
            except:
                pass
        
        from pages.cart_page import CartPage
        return CartPage(self.driver)
