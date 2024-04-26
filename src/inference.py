import gc
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from fusion_dict import * 

# model and adapters path
model_hf = "microsoft/BioGPT-Large"
lora_adapters = "mdelmas/BioGPT-Large-Natural-Products-RE-Diversity-synt-v1.0" # You can also try: mdelmas/BioGPT-Large-Natural-Products-RE-Extended-synt-v1.0

# Load model and plug adapters using peft
model = AutoModelForCausalLM.from_pretrained(model_hf, device_map={"":0})
model = PeftModel.from_pretrained(model, lora_adapters)
model = model.merge_and_unload()
tokenizer = AutoTokenizer.from_pretrained(model_hf)

def inference(doi,text,dict_triplet_doi_output):
    device = torch.device("cuda")

    # Decoding arguments
    EVAL_GENERATION_ARGS = {
        "max_length": 1024,
        "do_sample": False,
        "forced_eos_token_id": tokenizer.eos_token_id,
        "num_beams": 3,
        "early_stopping": "never",
        "length_penalty": 1.5,
        "temperature": 0
        }

    # Prepare the input
    input_text = text + tokenizer.eos_token + tokenizer.bos_token

    # Tokenize
    input_tokens = tokenizer(input_text, return_tensors='pt')
    input_tokens.to(device)

    # Generate
    with torch.no_grad():
        beam_output = model.generate(**input_tokens, **EVAL_GENERATION_ARGS)
    
    output = tokenizer.decode(beam_output[0][len(input_tokens["input_ids"][0]):], skip_special_tokens=True)
    
    dict_triplet_doi_output.setdefault(doi,[])
    dict_triplet_output = {}
    # Parse and print
    rels = output.strip().split(";")
    for rel in rels:
        data = rel.split("produces")
        if len(data)<2:
            print(f"can not manage : {data}")
            continue
        taxon = data[0].strip()
        metabolite = data[1].strip()
        dict_triplet_output.setdefault(taxon,[])
        if metabolite not in dict_triplet_output[taxon]:
            dict_triplet_output[taxon].append(metabolite)
    
    dict_triplet_doi_output[doi] = merge_dictionaries(dict_triplet_doi_output[doi],dict_triplet_output)
    
    torch.cuda.empty_cache()
    gc.collect()
