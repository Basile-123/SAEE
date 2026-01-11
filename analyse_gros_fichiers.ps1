# S'assurer qu'on est dans le bon dossier (celui du script)
Set-Location $PSScriptRoot

Write-Output "--- Etape 1 : Sélection du répertoire ---"
# Lancement du script python pour choisir le dossier
# On récupère la sortie standard (le chemin affiché par le print)
$rep_base = python select_folder.py

# Vérification si le répertoire est valide
if (-not [string]::IsNullOrWhiteSpace($rep_base) -and (Test-Path $rep_base)) {
    Write-Output "Répertoire sélectionné : $rep_base"
    
    Write-Output "--- Etape 2 : Analyse des fichiers (patience...) ---"
    # Appel du script d'analyse en passant le répertoire en argument
    python scan_files.py "$rep_base"

    Write-Output "--- Etape 3 : Affichage des résultats ---"
    # Appel du script d'affichage
    python display_results.py "$rep_base"
    
    Write-Output "Fin du programme."
}
else {
    Write-Output "Aucun répertoire sélectionné ou répertoire invalide."
}