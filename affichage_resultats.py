import json
import sys
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons

NB_MAXI_FICHIERS = 100
NB_LEGENDES_PAR_PAGE = 25
SCRIPT_SUPPRESSION = "suppression.ps1"

def lire_json(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)

def couleurs_aleatoires(n):
    return [QColor(random.randint(0,255),
                   random.randint(0,255),
                   random.randint(0,255)) for _ in range(n)]

def creation_script():
    lignes = [
        'Write-Output "Script PowerShell pour supprimer des fichiers"',
        '$rep = Read-Host "Confirmer la suppression (OUI)"',
        'if ($rep -eq "OUI") {'
    ]

    index = 0
    for leg in liste_legendes:
        etats = leg.recupere_etats_case_a_cocher()
        for etat in etats:
            if etat:
                chemin = fichiers[index][0]
                lignes.append(f' Remove-Item -Path "{chemin}" -Force')
            index += 1

    lignes.append('} else { Write-Output "Annulé" }')

    with open(SCRIPT_SUPPRESSION, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    fichiers = lire_json("resultats.json")
    couleurs = couleurs_aleatoires(len(fichiers))

    fenetre = Onglets()

    fromage = Camembert(fichiers, couleurs)
    fenetre.add_onglet("Camembert", fromage.dessine_camembert())

    liste_legendes = []
    for i in range(0, len(fichiers), NB_LEGENDES_PAR_PAGE):
        leg = Legendes(fichiers, couleurs, i)
        liste_legendes.append(leg)
        fenetre.add_onglet(
            f"Légende {i//NB_LEGENDES_PAR_PAGE + 1}",
            leg.dessine_legendes()
        )

    ihm = Boutons("Répertoire sélectionné", creation_script)
    fenetre.add_onglet("IHM", ihm.dessine_boutons())

    fenetre.show()
    sys.exit(app.exec_())
