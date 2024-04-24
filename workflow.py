import gc
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

from inference import * 

import argparse

# model and adapters path
model_hf = "microsoft/BioGPT-Large"
lora_adapters = "mdelmas/BioGPT-Large-Natural-Products-RE-Diversity-synt-v1.0" # You can also try: mdelmas/BioGPT-Large-Natural-Products-RE-Extended-synt-v1.0

# Load model and plug adapters using peft
model = AutoModelForCausalLM.from_pretrained(model_hf, device_map={"":0})
model = PeftModel.from_pretrained(model, lora_adapters)
model = model.merge_and_unload()
tokenizer = AutoTokenizer.from_pretrained(model_hf)

if __name__ == "__main__":
    # Créer un analyseur d'arguments
    parser = argparse.ArgumentParser(description='')

    # Ajouter des arguments
    parser.add_argument('--list_doi', type=str, help='list des doi')
    #parser.add_argument('arg2', type=int, help='---')
    #parser.add_argument('--option', type=str, help='Description de option')

    
    
    filtre_bool = lambda x: x != "N/A"
    list_clean_pmid = [x for x in list_pmid if filtre_bool(x)]
    
    for pmid in list_clean_pmid:
        print(pmid)
        get_title_abstract_text(pmid)
