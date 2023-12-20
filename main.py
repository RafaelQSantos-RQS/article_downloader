import pandas as pd
from modules.utilities import Utilities as ut
from modules.extract import Extraction as ex

#ut.setup_filesystem()
list_of_pubmed = pd.read_csv('data/processed/pubmed_list.csv')['pubmed_accession_number']
ex.extract_pmcid_from_pubmed(list_of_pubmed=list_of_pubmed,save_in='data/processed')