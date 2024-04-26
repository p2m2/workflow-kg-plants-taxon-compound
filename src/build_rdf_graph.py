from pygbif import registry,species
from ontology_mapping import init_ontology_mapping
from rdflib import Graph, Literal, RDF, URIRef, BNode
from rdflib.namespace import SKOS, RDFS, DCTERMS

import argparse
import os
import json
import sys 


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='')

    # Add arguments
    parser.add_argument('--dump_doi', type=str, help='JSON dump')
    parser.add_argument('--dump_taxon_compound', type=str, help='JSON dump')
    
    args = parser.parse_args()

    doi_taxon_compound_database = {}
    doi_article = {}

    dumpDoi = args.dump_doi
    dumpTaxonCoumpound = args.dump_taxon_compound

    # Check if the file exists
    if os.path.exists(dumpTaxonCoumpound):
        # Load JSON data from the file
        with open(dumpTaxonCoumpound, 'r') as file:
            doi_taxon_compound_database = json.load(file)
    else:
        sys.stderr.write(f"Error: The JSON file associating DOIs with pairs of 'taxon' and 'compound' is missing")
        sys.exit(1)
    
        # Check if the file exists
    if os.path.exists(dumpDoi):
        # Load JSON data from the file
        with open(dumpDoi, 'r') as file:
            doi_article_tmp = json.load(file)
        doi_article = { doi_article_tmp[x]['doi'] : doi_article_tmp[x] for x in doi_article_tmp }
    else:
        sys.stderr.write(f"Error: The JSON file associating PMIDs with DOIs is missing")
        sys.exit(1)

    classDict,propertyDict = init_ontology_mapping()
    g = Graph()

    for doiKey in doi_taxon_compound_database:
        
        if doiKey not in doi_article:
            sys.stderr.write(f"Error: doi {doiKey} is missing in {dumpDoi}")
            continue 

        doi = URIRef(f"https://doi.org/{doiKey}")
        ja = URIRef("http://purl.org/spar/fabio/JournalArticle")
        
        g.add((doi, RDF.type, ja))
        g.add((doi, DCTERMS.type, ja))
        g.add((doi, DCTERMS.title, Literal(doi_article[doiKey]['title'])))
        g.add((doi, DCTERMS.abstract, Literal(doi_article[doiKey]['abstract'])))
        
        for taxonKey in doi_taxon_compound_database[doiKey]:

            # Use GBIF API to define Taxon and attributes
            # -------------------------------------------
            backbone = species.name_backbone(name=taxonKey, kingdom='plants', strict=True)

            if backbone['matchType'] != 'NONE' and 'usageKey' in backbone :
                #print(backbone)
                taxon = URIRef(f"https://www.gbif.org/species/{backbone['usageKey']}")
                
                g.add((taxon, RDF.type, URIRef("http://schema.org/Taxon")))
                g.add((doi, DCTERMS.references, taxon))

                if 'kingdomKey' in backbone:
                    kingdom = URIRef(f"https://www.gbif.org/species/{backbone['kingdomKey']}")
                    g.add((taxon, URIRef(propertyDict['hasKingdom']), kingdom))
                    g.add((kingdom, RDFS.label, Literal(backbone['kingdom'])))
                
                if 'familyKey' in backbone:
                    family = URIRef(f"https://www.gbif.org/species/{backbone['familyKey']}")
                    g.add((taxon, URIRef(propertyDict['hasFamily']), family))
                    g.add((family, RDFS.label, Literal(backbone['family'])))

                if 'speciesKey' in backbone:
                    speci = URIRef(f"https://www.gbif.org/species/{backbone['speciesKey']}")
                    g.add((taxon, URIRef(propertyDict['hasSpecies']), speci))
                    g.add((speci, RDFS.label, Literal(backbone['species'])))

                if 'genusKey' in backbone:
                    genus = URIRef(f"https://www.gbif.org/species/{backbone['genusKey']}")
                    g.add((taxon, URIRef(propertyDict['hasGenus']), genus))
                    g.add((genus, RDFS.label, Literal(backbone['genus'])))

                if 'orderKey' in backbone:
                    order = URIRef(f"https://www.gbif.org/species/{backbone['orderKey']}")
                    g.add((taxon, URIRef(propertyDict['hasOrder']), order))
                    g.add((order, RDFS.label, Literal(backbone['order'])))

                if 'classKey' in backbone:
                    clas = URIRef(f"https://www.gbif.org/species/{backbone['classKey']}")
                    g.add((taxon, URIRef(propertyDict['hasClass']), clas))
                    g.add((clas, RDFS.label, Literal(backbone['class'])))

                if 'phylumKey' in backbone:
                    phylum = URIRef(f"https://www.gbif.org/species/{backbone['phylumKey']}")
                    g.add((taxon, URIRef(propertyDict['hasPhylum']), phylum))
                    g.add((phylum, RDFS.label, Literal(backbone['phylum'])))

                if 'rank' in backbone:
                    g.add((taxon, URIRef(propertyDict['hasRank']), Literal(backbone['rank'])))

                if 'scientificName' in backbone:
                    g.add((taxon, URIRef(propertyDict['hasScientificName']), Literal(backbone['scientificName'])))
                
                if 'canonicalName' in backbone:
                    g.add((taxon, URIRef(propertyDict['hasCanicalName']), Literal(backbone['canonicalName'])))
                
                n = BNode()
                ## Skos:related with compound
                for compound in doi_taxon_compound_database[doiKey][taxonKey]:    
                    g.add((n, SKOS.related, taxon))
                    g.add((n, SKOS.related, Literal(compound.strip())))

                g.add((taxon, URIRef("http://purl.org/spar/cito/hasCitingEntity"), n))

            

    print("--- printing ---")
    fileTtl = dumpDoi.split(".")[0]+".ttl"
    g.serialize(destination=fileTtl,format='ttl')
    print(f"-- {fileTtl} -- ")