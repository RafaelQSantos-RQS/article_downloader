import pandas as pd
from modules.utilities import setup_filesystem
from modules.transform import data_processing
from modules.extract import extract_pmcid_from_list
from modules.download import download_articles_from_list_of_pmcid

# Preparação do sistema de arquivos
setup_filesystem()

data_path = 'data/raw/DENV2_locus_pubmed.csv'

# Extraindo a lista de pubmed
df_pubmed_vs_locus = data_processing(data_path=data_path)

# Coletando os pmcid da lista de pubmed
list_of_pubmed = df_pubmed_vs_locus['Pubmed accession number'].unique()
extract_pmcid_from_list(list_of_pubmed=list_of_pubmed,number_of_webscrappers=3,headless=True,save_in='./data/processed')

# Baixando os artigos
#list_of_pmcid = set(pd.read_csv('data/processed/pubmed_vs_pmcid.csv')['pmcid'].dropna(axis=0))
#download_articles_from_list_of_pmcid(list_of_pmcid=list_of_pmcid,headless=False,save_in='data/raw/articles',max_workers=3)