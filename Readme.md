# Workflow KG Plants Taxon Compound

This workflow involves a chain of processes to construct a knowledge graph from a list of scientific article DOIs. It aims to establish connections between scientific articles contained in PubMed and pairs of taxa/metabolites through the "produces" relationship. This work is based on the repository [Relation Extraction in underexplored biomedical domains: A diversity-optimised sampling and synthetic data generation approach](https://github.com/idiap/abroad-re).

[![RDF Model](img/model_kg_plant_taxon_compound.png)](https://www.tldraw.com/v/IXSiv3uYFx3t3X2U6On8C?v=0,0,1920,921&p=page)

## 1 - Building DOI list file

- Search in PubMed for articles related to a taxon of the Brassicaceae family and glucosinolate compounds.

```bash
curl -s 'https://pubmed.ncbi.nlm.nih.gov/?term=brassica+glucosinolate&format=pubmed&size=200' | grep "\[doi\]" | cut -d" " -f3 > data/brassicale_glucosinolate.txt
```

## 2 - a) Building the article base from a list of DOIs

```
python src/api_doi.py --list_doi "10.1021/jf401802n,10.1021/jf405538d" --output test.json
```
## 2 - b) Building the article base from a list of DOIs in a file

```
python src/api_doi.py --list_doi_file data/list_doi_example.txt --output test.json
```

## 2 - c) Building tha article base from pdf article

*TODO*

## 3 - IDIAP Workflow to generate Taxon / Metabolite "produces" associations

- Working with a GPU environment

### Genouest Org

```bash
ssh $USER@genossh
srun --gpus 1 -p gpu --pty bash
. /local/env/envpython-3.9.5.sh
virtualenv ~/env-idiap ## only the first time !!
source ~/env-idiap/bin/activate 
export PATH=/home/genouest/inra_umr1349/$USER/.local/bin:$PATH
```

```bash
python src/workflow_idap.py --dump igepp.json
```

### References

- [Relation Extraction in underexplored biomedical domains: A diversity-optimised sampling and synthetic data generation approach](https://github.com/idiap/abroad-re)
- [colab](https://colab.research.google.com/github/idiap/abroad-re/blob/main/notebooks/inference.ipynb#scrollTo=6yPr04vYVoVE)

## 4 - Build RDF Graph

```bash
pip install pygbif rdflib
python src/build_rdf_graph.py --dump_doi test.json --dump_taxon_compound test_taxon_metabolite_associations_idiap.json
```

## Note about relation to build/infere

[gist](https://gist.github.com/ofilangi/b28b3da329f688fe32082e6418da79a0)
