import requests
import argparse
import json
import os 

# curl -d 'ids=10.1021/jf401802n,10.1021/jf405538d' 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?idtype=doi&format=json'

def search_pmid_from_doi(doi):
    base_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?idtype=doi"
    params = {
        "ids": doi,
        "idtype": "doi",  
        "format": "json"
    }
    pmid = ""
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('records', [])
        
        for article in articles:
            pmid = article.get('pmid', 'N/A')
    else:
        print("Error querying PubMed Central.")
    
    return doi, pmid

def get_title_abstract_text(doi_database, list_doi_pmid):
    print("get_title_abstract_text")
    list_articles = doi_database
    for doi, pmid in list_doi_pmid:
        print(doi, pmid)
        if pmid in doi_database:
            continue
        print("--request --")
        base_url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmid}/ascii"
        params = {}
        response = requests.get(base_url, params=params)
        
        list_articles[pmid] = {'doi' : doi}
        if response.status_code == 200:
            data = response.json()
            documents = data[0]['documents'] #
            for pardoc in documents:
                for passage in pardoc['passages']:
                    if ('infons' in passage and 'section_type' in passage['infons'] and
                        passage['infons']['section_type'] in [ 'TITLE','ABSTRACT','INTRO','RESULTS']):
                        key = passage['infons']['section_type'].lower()
                        list_articles[pmid].setdefault(key,"")
                        list_articles[pmid][key] += passage['text']
                        
        else:
            print("Error querying PubMed Central.")

    return list_articles


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='')

    # Add arguments
    parser.add_argument('--list_doi', type=str, help='list of DOIs separated by commas.')
    parser.add_argument('--list_doi_file', type=str, help='File containing a list of DOIs. Each DOI is on a separate line.')
    parser.add_argument('--output', type=str, help='JSON output results file')

    args = parser.parse_args()
    ldoi = []
    if args.list_doi != None :
        ldoi = args.list_doi.split(",")
    else:
         # Check if the file exists
        if os.path.exists(args.list_doi_file):
            # Load JSON data from the file
            with open(args.list_doi_file, 'r') as file:
                for line in file:
                    # Add the line (record) to the list
                    ldoi.append(line.strip())
    
    print(f"Number of DOIs:{len(ldoi)}")
    print(ldoi)
    # Path to the JSON output file
    output_file_path = args.output
    
    doi_database = {}

    # Check if the file exists
    if os.path.exists(output_file_path):
        # Load JSON data from the file
        with open(output_file_path, 'r') as file:
            doi_database = json.load(file)

    list_pmid = list(map(search_pmid_from_doi, ldoi))   
    filter_function = lambda pmid: pmid != 'N/A'

    list_clean_doi_pmid = [(doi, pmid) for doi, pmid in list_pmid if filter_function(pmid)]
    print(f"Clean list:{list_clean_doi_pmid}")
    article_results = get_title_abstract_text(doi_database, list_clean_doi_pmid)
  
    # Write JSON data to a file
    with open(output_file_path, 'w') as file:
        json.dump(article_results, file)

    print("The result has been written to the file:", output_file_path)
