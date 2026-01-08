Write-Output "Sélection du répertoire..."

$rep = python select_repertoire.py

if (-not $rep) {
    Write-Output "Aucun répertoire sélectionné"
    exit
}

if (-not (Test-Path $rep)) {
    Write-Output "Répertoire invalide"
    exit
}

python analyse_fichiers.py "$rep"
python affichage_resultats.py
