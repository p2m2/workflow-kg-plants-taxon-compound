from inference import * 

import argparse
import os
import json 

if __name__ == "__main__":
    # Créer un analyseur d'arguments
    parser = argparse.ArgumentParser(description='')

    # Ajouter des arguments
    parser.add_argument('--dump', type=str, help='JSON dum')
    
    args = parser.parse_args()

    article_database = {}

    # Vérifier si le fichier existe
    if os.path.exists(args.dump):
        # Charger les données JSON depuis le fichier
        with open(args.dump, 'r') as fichier:
            doi_database = json.load(fichier)
    
    for article in article_database:
        print(article)
