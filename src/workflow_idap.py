from inference import *

import argparse
import os
import json

def process_inference_n_words(doi, text, dict_results, n=350):
    words = text.split()
    
    chunk_size = n
    
    for i in range(0, len(words), chunk_size):
        word_chunk = words[i:i+chunk_size]
        inference(doi, ' '.join(word_chunk), dict_results)

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='')

    # Add arguments
    parser.add_argument('--dump', type=str, help='JSON dump')
    
    args = parser.parse_args()

    article_database = {}

    # Check if the file exists
    if os.path.exists(args.dump):
        # Load JSON data from the file
        with open(args.dump, 'r') as file:
            article_database = json.load(file)
    
    taxon_metabolite_relations = {}
   
    for pmid in article_database:
        if 'doi' not in article_database[pmid]:
            continue
        doi = article_database[pmid]['doi']
        if ('title' in article_database[pmid] and 
            'abstract' in article_database[pmid]):
            print(f"PMID {pmid} - {article_database[pmid]['title']}")
            print("-------------------------------------------------")
            text = article_database[pmid]['title'] + "."
            text += article_database[pmid]['abstract']
            process_inference_n_words(doi, text, taxon_metabolite_relations)
        
        if 'intro' in article_database[pmid]:
            text = article_database[pmid]['intro']
            process_inference_n_words(doi, text, taxon_metabolite_relations)

        #text = article_database[pmid]['results']
        #process_inference_n_words(text, taxon_metabolite_relations)
    
    outputfile = args.dump.split(".")[0] + "_taxon_metabolite_associations_idiap.json"
    if os.path.exists(outputfile):
        os.remove(outputfile)
    # Write JSON data to a file
    with open(outputfile, 'w') as file:
        json.dump(taxon_metabolite_relations, file)

    print(f"Results size: {str(len(taxon_metabolite_relations))}")
    print("The result has been written to the file:", outputfile)
