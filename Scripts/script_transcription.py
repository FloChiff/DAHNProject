#Ligne de commande pour l'exécution du script : python nom_du_script dossier_d'entrée dossier_de_sortie chemin_vers_le_modèle

import os
#Module pour travailler avec les fonctionnalités du système d'exploitation
import subprocess
#Module pour lancer de nouveaux processus
import sys
#Module pour communiquer avec le terminal
images = sys.argv[1]
#Création d'une variable pour stocker le chemin vers les images. Elle sera appelé comme deuxième argument dans le terminal.
file = os.listdir(images)
#Création d'une variable contenant une liste des éléments contenus dans le répertoire défini par la variable images (les images)
texts = sys.argv[2]
#Création d'une variable pour stocker le chemin vers le répertoire où seront créés les textes. Elle sera appelé comme troisième argument dans le terminal.
for img in file:
    complete_path = f"{images}/{img}"
    #Création d'une variable qui stocke le chemin vers les images à l'aide des variables précédemment déclarées
    output = f"{texts}/{img.replace('.JPG', '.txt')}"
    #Création d'une variable qui stocke le chemin vers les fichiers de sortie
    subprocess.run(["kraken", "-i", complete_path, output, "binarize", "segment", "ocr", "--model", sys.argv[3]])
    #Commande pour exécuter la transcription, avec les arguments présents entre crochets
    #À l'intérieur des crochets, on retrouve tous les éléments nécessaires à la transcription d'une image avec kraken
    #Soit kraken, le module input, le chemin vers les images à transcrire, le chemin de sortie, les commandes à exécuter pour la transcription, le module model et le chemin vers le modèle, appelé comme quatrième argument dans le terminal.