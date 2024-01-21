import pandas as pd
from modules.utilities import setup_filesystem
from modules.transform import data_processing
from modules.extract import extract_pmcid_from_list
from modules.download import download_articles_from_list_of_pmcid,webscraping_download_article_from_pmcid
from logging import info, error, INFO, basicConfig

basicConfig(level=INFO, format=f'%(asctime)s: %(message)s',datefmt='%d/%m/%Y %H:%M:%S')
def main():
    # Preparação do sistema de arquivos
    info(msg="## PREPARAÇÃO DO SISTEMA DE ARQUIVOS ##")
    setup_filesystem()

    # Extraindo a lista de pubmed
    info("## EXTRAINDO A LISTA DE PUBMEDS DO DATASET ##")
    data_path = 'data/raw/DENV2_locus_pubmed.csv'
    df_pubmed_vs_locus = data_processing(data_path=data_path)

    # Coletando os pmcid da lista de pubmed
    info("## COLETANDO OS PMCID DA LISTA DE PUBMED ##")
    list_of_pubmed = df_pubmed_vs_locus['Pubmed accession number'].unique()
    extract_pmcid_from_list(list_of_pubmed=list_of_pubmed,number_of_webscrappers=8,save_in='./data/processed')

    # Baixando os artigos
    info("## BAIXANDO OS ARTIGOS ##")
    list_of_pmcid = set(pd.read_csv('data/processed/pubmed_vs_pmcid.csv')['pmcid'].dropna(axis=0))
    download_articles_from_list_of_pmcid(list_of_pmcid=list_of_pmcid,headless=True,save_in='data/downloaded',max_workers=8)

if __name__ == '__main__':
    main()