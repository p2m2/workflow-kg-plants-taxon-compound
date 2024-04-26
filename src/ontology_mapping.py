import os 
import sys
import configparser


ontology_mapping_config_file = 'ontology_mapping.ini'

def assertIsNotNone(dict,value,errorMessage):
    if value not in dict :
        sys.stderr.write(f"[ontology_mapping] Error: {errorMessage} .")
        sys.exit(1)        

def init_ontology_mapping():
    config = configparser.ConfigParser()

    if os.path.exists(ontology_mapping_config_file):
        config.read(ontology_mapping_config_file)
    else:
        sys.stderr.write(f"Error: {ontology_mapping_config_file} file is missing.")
        sys.exit(1)
    
    if 'Class' not in config:
        sys.stderr.write(f"[ontology_mapping] Error: missing 'Class' category .")
        sys.exit(1)    
    
    if 'Property' not in config:
        sys.stderr.write(f"[ontology_mapping] Error: missing 'Property' category .")
        sys.exit(1)   

    classDict = config['Class']
    propertyDict = config['Property']

    ## check some values
    
    assertIsNotNone(classDict,'family', "Family value is missing or None")
    assertIsNotNone(classDict,'kingdom', "Kingdom value is missing or None")
    assertIsNotNone(classDict,'phylum', "Phylum value is missing or None")
    assertIsNotNone(classDict,'order', "Order value is missing or None")
    assertIsNotNone(classDict,'genus', "Genus value is missing or None")
    assertIsNotNone(classDict,'specy', "Species value is missing or None")
    assertIsNotNone(classDict,'class', "Class value is missing or None")

    assertIsNotNone(propertyDict,'hasRank', "Rank value is missing or None")
    assertIsNotNone(propertyDict,'hasScientificName', "ScientificName value is missing or None")
    assertIsNotNone(propertyDict,'hasCanicalName', "CanonicalName value is missing or None")

    return classDict,propertyDict
