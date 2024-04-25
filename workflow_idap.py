from inference import * 

import argparse
import os
import json 

def traitement_inference_n_mots(doi,texte,dict_results,n=350):
    mots = texte.split()
    
    taille_tranche = n
    
    for i in range(0, len(mots), taille_tranche):
        tranche_mots = mots[i:i+taille_tranche]
        inference(doi,' '.join(tranche_mots),dict_results)  


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
            article_database = json.load(fichier)
    
    relations_taxon_metabolite = {}
   
    for pmid in article_database:
        if 'doi' not in article_database[pmid]:
            continue
        doi = article_database[pmid]['doi']
        if ('title' in article_database[pmid] and 
            'abstract' in article_database[pmid] ) :
            print(f"PMID {pmid} - {article_database[pmid]['title']}")
            print("-------------------------------------------------")
            text = article_database[pmid]['title']+"."
            text += article_database[pmid]['abstract']
            traitement_inference_n_mots(doi,text,relations_taxon_metabolite)
        
        if 'intro' in article_database[pmid]:
            text = article_database[pmid]['intro']
            traitement_inference_n_mots(doi,text,relations_taxon_metabolite)

        #text = article_database[pmid]['results']
        #traitement_inference_n_mots(text,relations_taxon_metabolite)
    
    outputfile=args.dump.split(".")[0]+"_asso_taxon_metabolite_idiap.json"
    if os.path.exists(outputfile):
        os.remove(outputfile)
    # Écrire les données JSON dans un fichier
    with open(outputfile, 'w') as fichier:
        json.dump(relations_taxon_metabolite, fichier)

    print(f"size results:{str(len(relations_taxon_metabolite))}")
    print("Le résultat a été écrit dans le fichier :", outputfile)

