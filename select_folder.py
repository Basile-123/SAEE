import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from pathlib import Path

def selectionner_dossier():
    app = QApplication(sys.argv)
    dossier = QFileDialog.getExistingDirectory(None, "Sélectionnez un répertoire à analyser")
    
    if dossier:
        p = Path(dossier).resolve()
        print(p)
    
if __name__ == "__main__":
    selectionner_dossier()