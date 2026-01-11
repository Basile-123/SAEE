import sys
import json
from pathlib import Path

# Constantes
TAILLE_MINI_MIB = 10  # Seuil minimal exemple (10 MiB)
NB_MAXI_FICHIERS = 100

def get_files_recursively(base_path):
    """Retourne une liste de [chemin_str, taille_int]"""
    results = []
    base = Path(base_path)
    
    if not base.exists():
        return []

    # rglob('*') parcourt tout recursivement
    for file in base.rglob('*'):
        if file.is_file():
            try:
                size = file.stat().st_size
                # On ne garde que si > seuil (converti en octets)
                if size > TAILLE_MINI_MIB * 1024 * 1024:
                     # On stocke le chemin en string
                    results.append([str(file.resolve()), size])
            except PermissionError:
                pass # Ignorer les fichiers système protégés
    return results

def sort_files(file_list):
    """Tri décroissant sur la taille (index 1)"""
    return sorted(file_list, key=lambda x: x[1], reverse=True)

def filter_top_files(file_list, limit):
    """Slice pour garder les N premiers"""
    return file_list[:limit]

def save_json(data, filename="resultats.json"):
    """Sauvegarde en JSON en gérant les antislashs via la lib json standard"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Fichier JSON généré : {filename}")
    except Exception as e:
        print(f"Erreur JSON: {e}")

if __name__ == "__main__":
    # Le répertoire est passé en argument par PowerShell
    if len(sys.argv) > 1:
        rep_base = sys.argv[1]
    else:
        # Valeur par défaut pour tester sans PowerShell
        rep_base = "." 

    print(f"Analyse de : {rep_base}")
    files = get_files_recursively(rep_base)
    sorted_files = sort_files(files)
    top_files = filter_top_files(sorted_files, NB_MAXI_FICHIERS)
    save_json(top_files)