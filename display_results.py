import sys
import json
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor

# Import des classes fournies (On utilise les fichiers des profs tels quels)
from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons

FICHIER_JSON = "resultats.json"
NB_LEGENDES_PAR_PAGE = 25
NB_MAXI_FICHIERS = 100

def charger_json(fichier):
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def generer_couleurs(nb):
    couleurs = []
    for _ in range(nb):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        couleurs.append(QColor(r, g, b))
    return couleurs

class AppController:
    def __init__(self, liste_fichiers, liste_couleurs, repertoire_base):
        self.liste_fichiers = liste_fichiers
        self.liste_couleurs = liste_couleurs
        self.repertoire_base = repertoire_base
        self.pages_legendes = [] 

    def creation_script_suppression(self):
        print("Génération du script de suppression...")
        script_content = []
        
        script_content.append('Write-Output "Script PowerShell pour supprimer des fichiers sans confirmation"')
        script_content.append('Write-Output "Attention cette suppression est définitive..."')
        script_content.append('$reponse = Read-Host "Veuillez confirmer la suppression de tous ces fichiers: (OUI)"')
        script_content.append('if ($reponse -eq "OUI") {')
        script_content.append('    $confirmation = Read-Host "Etes-vous bien certain (e) ? (OUI)"')
        script_content.append('    if ($confirmation -eq "OUI") {')

        index_global = 0
        for page_legende in self.pages_legendes:
            # CORRECTION ICI : Le nom de la méthode dans le fichier prof est au pluriel
            etats = page_legende.recupere_etats_cases_a_cocher()
            
            for est_coche in etats:
                if est_coche and index_global < len(self.liste_fichiers):
                    chemin_fichier = self.liste_fichiers[index_global][0]
                    cmd = f'        Remove-Item -Path "{chemin_fichier}" -Force'
                    script_content.append(cmd)
                index_global += 1

        script_content.append('    } else {')
        script_content.append('        Write-Output "Opération annulée..."')
        script_content.append('    }')
        script_content.append('} else {')
        script_content.append('    Write-Output "Opération annulée..."')
        script_content.append('}')

        nom_script = "delete_files.ps1"
        with open(nom_script, "w", encoding="utf-8") as f:
            f.write("\n".join(script_content))
        print(f"Script {nom_script} créé avec succès.")

def main():
    app = QApplication(sys.argv)
    
    liste_fichiers = charger_json(FICHIER_JSON)
    if not liste_fichiers:
        liste_fichiers = []

    liste_couleurs = generer_couleurs(NB_MAXI_FICHIERS)
    rep_base = sys.argv[1] if len(sys.argv) > 1 else "Inconnu"

    controller = AppController(liste_fichiers, liste_couleurs, rep_base)

    fenetre = Onglets()

    if liste_fichiers:
        fromage = Camembert(liste_fichiers, liste_couleurs)
        layout_fromage = fromage.dessine_camembert()
        fenetre.add_onglet("Camembert", layout_fromage)

        nb_pages = (len(liste_fichiers) + NB_LEGENDES_PAR_PAGE - 1) // NB_LEGENDES_PAR_PAGE
        
        for i in range(nb_pages):
            num_start = i * NB_LEGENDES_PAR_PAGE
            
            # CORRECTION ICI : On ajoute le 4ème argument (NB_LEGENDES_PAR_PAGE)
            # car le fichier Creation_Legendes.py des profs l'exige.
            leg_page = Legendes(liste_fichiers, liste_couleurs, num_start, NB_LEGENDES_PAR_PAGE)
            
            controller.pages_legendes.append(leg_page)
            layout_leg = leg_page.dessine_legendes()
            fenetre.add_onglet(f"Légende {i+1}", layout_leg)

    ihm = Boutons(rep_base, controller.creation_script_suppression)
    layout_ihm = ihm.dessine_boutons()
    fenetre.add_onglet("IHM", layout_ihm)

    fenetre.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()