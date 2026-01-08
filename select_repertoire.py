from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
from pathlib import Path

def choisir_repertoire():
    app = QApplication(sys.argv)
    dossier = QFileDialog.getExistingDirectory(
        None,
        "Sélectionner le répertoire de base"
    )
    if dossier:
        print(Path(dossier).resolve())
    else:
        print("")

if __name__ == "__main__":
    choisir_repertoire()
