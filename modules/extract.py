import pandas as pd
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'https://pubmed.ncbi.nlm.nih.gov'

class Extraction:
    '''
    '''
    @staticmethod
    def extract_pcmid(pubmed:str):
        '''
        '''
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            url = f'{BASE_URL}/{pubmed}'
            page.goto(url=url)
            if page.locator("#full-view-identifiers li").filter(has_text="PMCID").count() > 0:
                pmcid = page.locator("#full-view-identifiers li").filter(has_text="PMCID").inner_text().replace('PMCID: ','').strip()
                result =  {'pubmed_accession_number': str(pubmed), 'pmcid': pmcid}
            else:
                result = {'pubmed_accession_number': str(pubmed), 'pmcid': None}
            
            browser.close()

            return result

    @staticmethod
    def extract_pmcid_from_list(list_of_pubmed:list[str],number_of_webscrappers:int=1,save_in:str='.'):
        '''
        '''
        dataframe = pd.DataFrame(columns=['pubmed_accession_number', 'pmcid'])
        with ThreadPoolExecutor(max_workers=number_of_webscrappers) as executor:
            results = list(executor.map(Extraction.extract_pcmid, list_of_pubmed))

        for result in results:
            row = pd.Series(result)
            dataframe = pd.concat([dataframe,row.to_frame().T],ignore_index=True)
        
        dataframe.to_csv(save_in + '/pubmed_vs_pmcid.csv', index=False)
