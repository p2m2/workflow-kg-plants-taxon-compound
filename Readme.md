# workflow-kg-plants-taxon-compound
## Construction de la base d'article 

```
python api_doi.py --list_doi "10.1021/jf401802n,10.1021/jf405538d" --output test.jso
```

## Maxime tools

[colab](https://colab.research.google.com/github/idiap/abroad-re/blob/main/notebooks/inference.ipynb#scrollTo=6yPr04vYVoVE)


### Genouest Org

- acess GPU env.

`ssh ofilangi@genossh`

```bash
srun --gpus 1 -p gpu --pty bash
. /local/env/envpython-3.9.5.sh
virtualenv ~/env-idiap
export PATH=/home/genouest/inra_umr1349/ofilangi/.local/bin:$PATH
```

```bash
pip install transformers
pip install peft
pip install sacremoses
```

### Load Model

```python
import gc
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# model and adapters path
model_hf = "microsoft/BioGPT-Large"
lora_adapters = "mdelmas/BioGPT-Large-Natural-Products-RE-Diversity-synt-v1.0" # You can also try: mdelmas/BioGPT-Large-Natural-Products-RE-Extended-synt-v1.0

# Load model and plug adapters using peft
model = AutoModelForCausalLM.from_pretrained(model_hf, device_map={"":0})
model = PeftModel.from_pretrained(model, lora_adapters)
model = model.merge_and_unload()
tokenizer = AutoTokenizer.from_pretrained(model_hf)
```
### Define Inference Function

```python
def inference(text):
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

  # Parse and print
  rels = output.strip().split("; ")
  for rel in rels:
    print("- " + rel)
  torch.cuda.empty_cache()
  gc.collect()
```

```python
title_text = "Producers and important dietary sources of ochratoxin A and citrinin."
abstract_text = "Land-adapted plants appeared between about 480 and 360 million years ago in the mid-Palaeozoic era, originating from charophycean green algae. The successful adaptation to land of these prototypes of amphibious plants - when they emerged from an aquatic environment onto the land - was achieved largely by massive formation of \"phenolic UV light screens\". In the course of evolution, plants have developed the ability to produce an enormous number of phenolic secondary metabolites, which are not required in the primary processes of growth and development but are of vital importance for their interaction with the environment, for their reproductive strategy and for their defense mechanisms. From a biosynthetic point of view, beside methylation catalyzed by O-methyltransferases, acylation and glycosylation of secondary metabolites, including phenylpropanoids and various derived phenolic compounds, are fundamental chemical modifications. Such modified metabolites have altered polarity, volatility, chemical stability in cells but also in solution, ability for interaction with other compounds (co-pigmentation) and biological activity. The control of the production of plant phenolics involves a matrix of potentially overlapping regulatory signals. These include developmental signals, such as during lignification of new growth or the production of anthocyanins during fruit and flower development, and environmental signals for protection against abiotic and biotic stresses. For some of the key compounds, such as the flavonoids, there is now an excellent understanding of the nature of those signals and how the signal transduction pathway connects through to the activation of the phenolic biosynthetic genes. Within the plant environment, different microorganisms can coexist that can establish various interactions with the host plant and that are often the basis for the synthesis of specific phenolic metabolites in response to these interactions. In the rhizosphere, increasing evidence suggests that root specific chemicals (exudates) might initiate and manipulate biological and physical interactions between roots and soil organisms. These interactions include signal traffic between roots of competing plants, roots and soil microbes, and one-way signals that relate the nature of chemical and physical soil properties to the roots. Plant phenolics can also modulate essential physiological processes such as transcriptional regulation and signal transduction. Some interesting effects of plant phenolics are also the ones associated with the growth hormone auxin. An additional role for flavonoids in functional pollen development has been observed. Finally, anthocyanins represent a class of flavonoids that provide the orange, red and blue/purple colors to many plant tissues. According to the coevolution theory, red is a signal of the status of the tree to insects that migrate to (or move among) the trees in autumn."
text = title_text + " " + abstract_text
inference(text)
```