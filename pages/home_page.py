"""
HomePage : Page d'accueil de Tunisianet
Gère la navigation et la recherche de produits
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page d'accueil du site Tunisianet"""
    
    # Sélecteurs
    SEARCH_BOX = (By.XPATH, "//input[@type='search' or @name='s' or contains(@placeholder, 'recherche') or contains(@class, 'search')]")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit' and (contains(@class, 'search') or contains(text(), 'Rechercher'))]")
    LOGO = (By.XPATH, "//a[contains(@class, 'logo') or contains(@href, 'tunisianet')]//img | //img[contains(@alt, 'Tunisianet') or contains(@src, 'logo')]")
    CATEGORY_LINKS = (By.XPATH, "//a[contains(@href, 'categorie') or contains(@href, 'category')] | //nav//a[contains(@href, '/')] | //ul[contains(@class, 'menu')]//a")
    
    def __init__(self, driver):
       
        super().__init__(driver)
        self.base_url = "https://www.tunisianet.com.tn"
    
    def navigate_to_home(self):
        
        self.driver.get(self.base_url)
        return self
    
    def verify_page_loaded(self):
        
        # Vérifier que la barre de recherche est présente
        search_present = self.is_element_present(*self.SEARCH_BOX)
        # Vérifier que le logo est présent (optionnel, peut ne pas être présent)
        logo_present = self.is_element_present(*self.LOGO)
        
        return search_present or logo_present
    
    def search_product(self, product_name):
        
        # Essayer plusieurs sélecteurs pour la barre de recherche
        search_selectors = [
            (By.XPATH, "//input[@type='search']"),
            (By.XPATH, "//input[@name='s']"),
            (By.XPATH, "//input[contains(@placeholder, 'recherche') or contains(@placeholder, 'Recherche')]"),
            (By.XPATH, "//input[contains(@class, 'search') or contains(@id, 'search')]"),
            (By.XPATH, "//input[@type='text' and contains(@class, 'search')]"),
        ]
        
        search_found = False
        for selector in search_selectors:
            try:
                if self.is_element_present(*selector, timeout=2):
                    self.send_keys(*selector, product_name)
                    search_found = True
                    break
            except:
                continue
        
        if not search_found:
            raise Exception("Barre de recherche non trouvée")
        
        # Essayer plusieurs méthodes pour lancer la recherche
        # 1. Chercher un bouton de recherche
        search_button_selectors = [
            (By.XPATH, "//button[@type='submit' and contains(@class, 'search')]"),
            (By.XPATH, "//button[contains(@class, 'search')]"),
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//i[contains(@class, 'search')]/parent::button"),
        ]
        
        button_found = False
        for selector in search_button_selectors:
            try:
                if self.is_element_present(*selector, timeout=2):
                    self.click(*selector)
                    button_found = True
                    break
            except:
                continue
        
        # 2. Si pas de bouton, appuyer sur Entrée
        if not button_found:
            from selenium.webdriver.common.keys import Keys
            element = self.find_element(*search_selectors[0])
            element.send_keys(Keys.RETURN)
        
        # Importer ResultsPage ici pour éviter les imports circulaires
        from pages.results_page import ResultsPage
        return ResultsPage(self.driver)
    
    def navigate_to_category(self, category_name=None):
        
        import time
        time.sleep(1)  # Attendre que la page soit complètement chargée
        
        # Sélecteurs pour trouver les liens de catégories
        category_selectors = [
            (By.XPATH, f"//a[contains(text(), '{category_name}') and (contains(@href, 'categorie') or contains(@href, 'category'))]") if category_name else None,
            (By.XPATH, "//a[contains(@href, 'categorie') or contains(@href, 'category')]"),
            (By.XPATH, "//nav//a[contains(@href, '/') and not(contains(@href, '#'))]"),
            (By.XPATH, "//ul[contains(@class, 'menu')]//a[contains(@href, '/')]"),
            (By.XPATH, "//div[contains(@class, 'category')]//a"),
        ]
        
        category_found = False
        for selector in category_selectors:
            if selector is None:
                continue
            try:
                if category_name:
                    # Chercher un lien avec le nom de la catégorie
                    links = self.find_elements(*selector)
                    for link in links:
                        if category_name.lower() in link.text.lower():
                            link.click()
                            category_found = True
                            break
                    if category_found:
                        break
                else:
                    # Prendre le premier lien de catégorie trouvé
                    if self.is_element_present(*selector, timeout=3):
                        links = self.find_elements(*selector)
                        if links and len(links) > 0:
                            # Éviter les liens vers la page d'accueil
                            for link in links:
                                href = link.get_attribute('href') or ''
                                if href and 'tunisianet' in href.lower() and href != self.base_url and href != f"{self.base_url}/":
                                    link.click()
                                    category_found = True
                                    break
                            if category_found:
                                break
            except:
                continue
        
        if not category_found:
            raise Exception("Aucun lien de catégorie trouvé")
        
        # Importer CategoryPage ici pour éviter les imports circulaires
        from pages.category_page import CategoryPage
        return CategoryPage(self.driver)
    
    def extract_all_navigation_links(self):
        
        import time
        time.sleep(2)  # Attendre que la page soit complètement chargée
        
        all_links = []
        seen_urls = set()
        
        # Sélecteurs pour trouver tous les liens de navigation
        link_selectors = [
            (By.XPATH, "//a[@href]"),  # Tous les liens avec href
            (By.XPATH, "//nav//a[@href]"),  # Liens dans les menus de navigation
            (By.XPATH, "//ul[contains(@class, 'menu')]//a[@href]"),  # Liens dans les menus
            (By.XPATH, "//div[contains(@class, 'category')]//a[@href]"),  # Liens de catégories
            (By.XPATH, "//div[contains(@class, 'nav')]//a[@href]"),  # Liens dans les divs de navigation
        ]
        
        for selector in link_selectors:
            try:
                links = self.find_elements(*selector)
                for link in links:
                    try:
                        href = link.get_attribute('href')
                        text = link.text.strip()
                        
                        if not href:
                            continue
                        
                        # Normaliser l'URL
                        href = href.strip()
                        
                        # Filtrer les liens non pertinents
                        if self._is_valid_link(href):
                            # Éviter les doublons
                            if href not in seen_urls:
                                seen_urls.add(href)
                                all_links.append({
                                    'href': href,
                                    'text': text if text else href
                                })
                    except:
                        continue
            except:
                continue
        
        return all_links
    
    def _is_valid_link(self, href):
        """
        Vérifie si un lien est valide pour être testé
        
        Args:
            href: URL du lien
            
        Returns:
            bool: True si le lien est valide
        """
        if not href:
            return False
        
        href_lower = href.lower()
        
        # Exclure les liens non pertinents
        exclude_patterns = [
            '#',  # Ancres
            'javascript:',  # JavaScript
            'mailto:',  # Email
            'tel:',  # Téléphone
            'whatsapp',  # WhatsApp
            'facebook',  # Réseaux sociaux
            'twitter',
            'instagram',
            'youtube',
            'linkedin',
            'pinterest',
            'tiktok',
            'snapchat',
        ]
        
        for pattern in exclude_patterns:
            if pattern in href_lower:
                return False
        
        # Vérifier que c'est un lien du site Tunisianet
        if 'tunisianet.com.tn' not in href_lower:
            return False
        
        # Exclure la page d'accueil (déjà testée)
        if href_lower == self.base_url.lower() or href_lower == f"{self.base_url.lower()}/":
            return False
        
        # Inclure les liens vers des pages de catégories, produits, etc.
        include_patterns = [
            '/categorie',
            '/category',
            '/produit',
            '/product',
            '/informatique',
            '/telephonie',
            '/stockage',
            '/impression',
            '/tv-son-photos',
            '/electromenager',
            '/reseau',
            '/securite',
            '/bureautique',
        ]
        
        # Si le lien contient un pattern inclus, il est valide
        for pattern in include_patterns:
            if pattern in href_lower:
                return True
        
        # Si le lien est une URL relative ou absolue du site, l'inclure aussi
        if href_lower.startswith('/') or href_lower.startswith('http'):
            # Mais exclure les liens vers des fichiers (images, PDF, etc.)
            exclude_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.exe', '.css', '.js']
            if any(href_lower.endswith(ext) for ext in exclude_extensions):
                return False
            return True
        
        return False
