from pathlib import Path
import json
import sys

TAILLE_MINI_MIB = 1
NB_MAXI_FICHIERS = 100

def analyse_arborescence(repertoire_base):
    fichiers = []
    for f in Path(repertoire_base).rglob("*"):
        if f.is_file():
            fichiers.append([str(f.resolve()), f.stat().st_size])
    return fichiers

def tri_decroissant(liste):
    return sorted(liste, key=lambda x: x[1], reverse=True)

def filtrage(liste, taille_mib, nb_max):
    taille_octets = taille_mib * 1048576
    resultat = [f for f in liste if f[1] >= taille_octets]
    return resultat[:nb_max]

def sauvegarde_json(liste, nom_fichier):
    for f in liste:
        f[0] = f[0].replace("\\", "\\\\")
    with open(nom_fichier, "w", encoding="utf-8") as fp:
        json.dump(liste, fp, indent=2)

if __name__ == "__main__":
    repertoire = sys.argv[1]
    fichiers = analyse_arborescence(repertoire)
    fichiers = tri_decroissant(fichiers)
    fichiers = filtrage(fichiers, TAILLE_MINI_MIB, NB_MAXI_FICHIERS)
    sauvegarde_json(fichiers, "resultats.json")
