import pandas as pd
import modules.utilities as utils
import modules.extract as ex
import modules.download as dw

# Preparação do sistema de arquivos
utils.setup_filesystem()

# Extraindo a lista de pubmed
list_of_pubmed = pd.read_csv('data/processed/pubmed_list.csv')['pubmed_accession_number']

# Coletando os pmcid da lista de pubmed
ex.extract_pmcid_from_list(list_of_pubmed=list_of_pubmed,number_of_webscrappers=3,save_in='./data/processed')

# Baixando os artigos
list_of_pmcid = set(pd.read_csv('data/processed/pubmed_vs_pmcid.csv')['pmcid'].dropna(axis=0))
dw.download_articles_from_list_of_pmcid(list_of_pmcid=list_of_pmcid,headless=False,save_in='data/raw/articles',max_workers=3)