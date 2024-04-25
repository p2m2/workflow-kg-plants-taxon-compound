# Workflow KG Plants Taxon Compound

This workflow involves a chain of processes to construct a knowledge graph from a list of scientific article DOIs. It aims to establish connections between scientific articles contained in PubMed and pairs of taxa/metabolites through the "produces" relationship. This work is based on the repository [Relation Extraction in underexplored biomedical domains: A diversity-optimised sampling and synthetic data generation approach](https://github.com/idiap/abroad-re).

## 1 - a) Building the article base from a list of DOIs

```
python api_doi.py --list_doi "10.1021/jf401802n,10.1021/jf405538d" --output test.jso
```
## 1 - b) Building the article base from a list of DOIs in a file

```
python api_doi.py --list_doi_file list_doi_example.txt --output test.jso
```

## 2 - IDIAP Workflow to generate Taxon / Metabolite "produces" associations

- Working with a GPU environment

### Genouest Org

```bash
ssh $USER@genossh
srun --gpus 1 -p gpu --pty bash
. /local/env/envpython-3.9.5.sh
virtualenv ~/env-idiap
source ~/env-idiap/bin/activate
export PATH=/home/genouest/inra_umr1349/$USER/.local/bin:$PATH
```

```bash
python workflow_idap.py --dump igepp.json
```

### References
- 
[colab](https://colab.research.google.com/github/idiap/abroad-re/blob/main/notebooks/inference.ipynb#scrollTo=6yPr04vYVoVE)

## 3 - GBIF association with taxon

## 4 - Metabolite association with 
