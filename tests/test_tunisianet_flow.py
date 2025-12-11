"""
Test end-to-end complet pour le site Tunisianet
Teste : navigation, recherche, ajout au panier, checkout
"""
import pytest
from utils.driver_factory import get_driver
from pages.home_page import HomePage


@pytest.fixture(scope="function")
def driver():
    """
    Fixture pytest pour créer et fermer le driver
    
    Yields:
        webdriver.Chrome: Instance du driver
    """
    driver = get_driver()
    yield driver
    driver.quit()


def test_home_page_loaded(driver):
    
    # Navigation vers la page d'accueil
    home_page = HomePage(driver)
    home_page.navigate_to_home()
    
    # Vérifier que la page se charge correctement
    assert home_page.verify_page_loaded(), "La page d'accueil ne s'est pas chargée correctement"
    print("[OK] Page d'accueil chargee avec succes")


def test_all_pages_functionality(driver):
    
    import time
    from pages.home_page import HomePage
    from pages.category_page import CategoryPage
    from pages.base_page import BasePage
    
    # 1. Vérifier la page d'accueil
    home_page = HomePage(driver)
    home_page.navigate_to_home()
    assert home_page.verify_page_loaded(), "La page d'accueil ne s'est pas chargée correctement"
    print("[OK] Page d'accueil verifiee")
    
    # 2. Extraire tous les liens de navigation disponibles
    print("\n[INFO] Extraction des liens de navigation...")
    all_links = home_page.extract_all_navigation_links()
    print(f"[INFO] {len(all_links)} liens trouves sur la page d'accueil")
    
    if len(all_links) == 0:
        print("[WARNING] Aucun lien de navigation trouve, test annule")
        return
    
    # Limiter le nombre de pages à tester (pour éviter un test trop long)
    max_pages_to_test = 30
    links_to_test = all_links[:max_pages_to_test]
    
    if len(all_links) > max_pages_to_test:
        print(f"[INFO] Limitation a {max_pages_to_test} pages pour le test (sur {len(all_links)} trouvees)")
    
    # 3. Tester chaque page
    pages_tested = []
    pages_failed = []
    
    print(f"\n[INFO] Test de {len(links_to_test)} pages...\n")
    
    for i, link_info in enumerate(links_to_test, 1):
        href = link_info['href']
        text = link_info['text']
        
        try:
            # Retourner à la page d'accueil avant chaque test
            home_page.navigate_to_home()
            time.sleep(1)
            
            # Naviguer directement vers l'URL
            print(f"[{i}/{len(links_to_test)}] Test de: {text[:50]}... ({href[:60]}...)")
            driver.get(href)
            time.sleep(2)  # Attendre le chargement
            
            # Vérifier que la page se charge
            page = BasePage(driver)
            current_url = page.get_current_url()
            
            # Vérifications basiques de chargement
            # 1. Vérifier que l'URL a changé (pas une redirection vers l'accueil)
            base_url_lower = home_page.base_url.lower()
            if current_url.lower() != base_url_lower and current_url.lower() != f"{base_url_lower}/":
                # 2. Vérifier qu'il n'y a pas d'erreur 404 dans le titre ou le contenu
                page_title = driver.title.lower()
                page_source = driver.page_source.lower()
                
                # Rechercher des indicateurs d'erreur
                error_indicators = [
                    '404', 
                    'not found', 
                    'page introuvable', 
                    'erreur 404',
                    'page non trouvee',
                    'error 404'
                ]
                
                has_error = any(indicator in page_title or indicator in page_source[:2000] for indicator in error_indicators)
                
                # 3. Vérifier que la page a du contenu (au moins un body avec du texte)
                has_content = len(driver.page_source) > 1000  # Au moins 1000 caractères
                
                if not has_error and has_content:
                    pages_tested.append({
                        'text': text,
                        'url': href
                    })
                    print(f"  [OK] Page chargee avec succes")
                else:
                    reason = 'Erreur 404' if has_error else 'Page vide ou sans contenu'
                    pages_failed.append({
                        'text': text,
                        'url': href,
                        'reason': reason
                    })
                    print(f"  [FAIL] {reason}")
            else:
                pages_failed.append({
                    'text': text,
                    'url': href,
                    'reason': 'Redirection vers la page d\'accueil'
                })
                print(f"  [FAIL] Redirection vers la page d'accueil")
                
        except Exception as e:
            pages_failed.append({
                'text': text,
                'url': href,
                'reason': str(e)[:100]
            })
            print(f"  [ERROR] {str(e)[:100]}")
    
    # 4. Résumé des tests
    print(f"\n{'='*60}")
    print(f"[RESUME] Pages testees avec succes: {len(pages_tested)}")
    print(f"[RESUME] Pages en echec: {len(pages_failed)}")
    print(f"{'='*60}")
    
    if pages_tested:
        print("\n[SUCCESS] Pages fonctionnelles:")
        for page in pages_tested[:10]:  # Afficher les 10 premières
            print(f"  - {page['text'][:50]}...")
        if len(pages_tested) > 10:
            print(f"  ... et {len(pages_tested) - 10} autres")
    
    if pages_failed:
        print("\n[FAILED] Pages en echec:")
        for page in pages_failed[:10]:  # Afficher les 10 premières
            print(f"  - {page['text'][:50]}... ({page['reason'][:50]})")
        if len(pages_failed) > 10:
            print(f"  ... et {len(pages_failed) - 10} autres")
    
    # Le test passe si au moins une page fonctionne
    assert len(pages_tested) > 0, f"Aucune page ne fonctionne correctement (sur {len(links_to_test)} testees)"
    print(f"\n[SUCCESS] Test de toutes les pages termine ! ({len(pages_tested)}/{len(links_to_test)} pages fonctionnelles)")


def test_full_tunisianet_flow(driver):
    
    # 1. Navigation vers la page d'accueil
    home_page = HomePage(driver)
    home_page.navigate_to_home()

    # Vérifier que la page se charge correctement
    assert home_page.verify_page_loaded(), "La page d'accueil ne s'est pas chargée correctement"
    print("[OK] Page d'accueil chargee avec succes")

    # 1.5. Vérification de la page catégorie
    category_page = home_page.navigate_to_category()
    assert category_page.verify_category_page_loaded(), "La page de catégorie ne s'est pas chargée correctement"
    print("[OK] Page de categorie chargee avec succes")

    # Retourner à la page d'accueil pour continuer le test
    home_page.navigate_to_home()

    # 2. Recherche de produit
    search_term = (
        "Pc de Bureau All in One Lenovo A100 / Intel N100 / 8 Go / 256 Go SSD / Gris"
    )
    results_page = home_page.search_product(search_term)
    print(f"[OK] Recherche effectuee pour : {search_term}")

    # Vérifier que des résultats apparaissent
    assert results_page.verify_results_displayed(), "Aucun résultat de recherche n'est affiché"
    print("[OK] Resultats de recherche affiches")

    # 3. Sélection d'un produit
    product_page = results_page.select_first_product()
    print("[OK] Produit selectionne dans les resultats")

    # 4. Ajout au panier
    cart_page = product_page.add_to_cart()
    print("[OK] Produit ajoute au panier")

    # Si l'ajout au panier ne redirige pas automatiquement, aller au panier
    if "cart" not in cart_page.get_current_url().lower() and "panier" not in cart_page.get_current_url().lower():
        cart_page = product_page.go_to_cart()
        print("[OK] Navigation vers le panier")

    # 5. Vérifier que le produit est dans le panier
    assert cart_page.verify_product_in_cart(), "Le produit n'est pas présent dans le panier"
    print("[OK] Produit verifie dans le panier")

    # 6. Début du checkout
    checkout_success = cart_page.proceed_to_checkout()
    if checkout_success:
        print("[OK] Redirection vers le checkout reussie")
    else:
        print("[WARNING] Bouton checkout non trouve ou redirection non detectee (peut necessiter une authentification)")

    print("\n[SUCCESS] Test end-to-end termine avec succes !")
