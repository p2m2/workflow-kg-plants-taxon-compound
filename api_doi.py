import requests
import argparse
import json
import os 

#curl -d 'ids=10.1021/jf401802n,10.1021/jf405538d' 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?idtype=doi&format=json

def search_pmid_from_doi(doi_list):
    base_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?idtype=doi"
    params = {
        "ids": doi_list,
        "idtype": "doi",  
        "format": "json"
    }
    pmid_list = []
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('records', [])
        for article in articles:
            pmid = article.get('pmid', 'N/A')
            pmid_list.append(pmid)
    else:
        print("Erreur lors de la requête à PubMed Central.")
    
    return pmid_list

def get_title_abstract_text(doi_database,list_pmid):

    list_article = doi_database

    for pmid in list_pmid:
        base_url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmid}/ascii"
        params = {}
        response = requests.get(base_url, params=params)
        
        list_article[pmid] = {}

        if response.status_code == 200:
            data = response.json()
            documents = data[0]['documents'] #
            for pardoc in documents:
                for passage in pardoc['passages']:
                    if ('infons' in passage and 'section_type' in passage['infons'] and
                        passage['infons']['section_type'] in [ 'TITLE','ABSTRACT','INTRO','RESULTS']):
                        key = passage['infons']['section_type'].lower()
                        list_article[pmid].setdefault(key,"")
                        list_article[pmid][key] += passage['text']
                        
        else:
            print("Erreur lors de la requête à PubMed Central.")

    return list_article


if __name__ == "__main__":
    # Créer un analyseur d'arguments
    parser = argparse.ArgumentParser(description='')

    # Ajouter des arguments
    parser.add_argument('--list_doi', type=str, help='list des doi')
    parser.add_argument('--output', type=str, help='json output results file')

    args = parser.parse_args()
    
     # Chemin vers le fichier de sortie JSON
    chemin_fichier = args.output
    
    doi_database = {}

    # Vérifier si le fichier existe
    if os.path.exists(chemin_fichier):
        # Charger les données JSON depuis le fichier
        with open(chemin_fichier, 'r') as fichier:
            doi_database = json.load(fichier)

    list_pmid = search_pmid_from_doi(args.list_doi.split(","))
    
    filtre_bool = lambda x: x != "N/A"

    list_clean_pmid = [x for x in list_pmid if filtre_bool(x)]
    
    resultats_articles = get_title_abstract_text(doi_database,list_clean_pmid)
  
   

    # Écrire les données JSON dans un fichier
    with open(chemin_fichier, 'w') as fichier:
        json.dump(resultats_articles, fichier)

    print("Le résultat a été écrit dans le fichier :", chemin_fichier)

    
