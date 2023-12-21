import pandas as pd
from modules.utilities import Utilities as ut
from modules.extract import Extraction as ex

#ut.setup_filesystem()
list_of_pubmed = pd.read_csv('data/processed/pubmed_list.csv')['pubmed_accession_number']
ex.extract_pmcid_from_list(list_of_pubmed=list_of_pubmed,number_of_webscrappers=6,save_in='./data/processed')