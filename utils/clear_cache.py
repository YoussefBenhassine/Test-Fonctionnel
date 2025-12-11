"""
Script utilitaire pour nettoyer le cache de webdriver-manager
Utile si le chromedriver téléchargé est corrompu
"""
import shutil
import os
from pathlib import Path

def clear_webdriver_cache():
    
    # Chemins possibles du cache webdriver-manager
    possible_paths = [
        Path.home() / '.wdm',
        Path.home() / '.cache' / 'selenium',
    ]
    
    # Sur Windows, aussi vérifier dans AppData
    if os.name == 'nt':
        appdata = os.environ.get('APPDATA', '')
        if appdata:
            possible_paths.append(Path(appdata) / '.wdm')
        localappdata = os.environ.get('LOCALAPPDATA', '')
        if localappdata:
            possible_paths.append(Path(localappdata) / '.wdm')
    
    cache_found = False
    for cache_path in possible_paths:
        if cache_path.exists():
            try:
                shutil.rmtree(cache_path)
                print(f"[OK] Cache webdriver-manager supprime : {cache_path}")
                cache_found = True
            except Exception as e:
                print(f"[ERREUR] Erreur lors de la suppression de {cache_path} : {e}")
    
    if cache_found:
        print("Le prochain lancement telechargera une nouvelle version du driver.")
    else:
        print("[INFO] Aucun cache webdriver-manager trouve.")

if __name__ == "__main__":
    clear_webdriver_cache()

