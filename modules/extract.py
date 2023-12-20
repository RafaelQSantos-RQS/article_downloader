import pandas as pd
from playwright.sync_api import sync_playwright

class Extraction:
    '''
    '''
    @staticmethod
    def extract_pmcid_from_pubmed(list_of_pubmed:list[str],save_in:str='.'):
        '''
        '''
        base_url = 'https://pubmed.ncbi.nlm.nih.gov'
        dataframe = pd.DataFrame(columns=['pubmed_accession_number','pmcid'])
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            for pubmed in list_of_pubmed:
                url = f'{base_url}/{pubmed}'
                page.goto(url=url)
                if page.locator("#full-view-identifiers li").filter(has_text="PMCID").count() > 0:
                    pmcid = page.locator("#full-view-identifiers li").filter(has_text="PMCID").inner_text().replace('PMCID: ','').strip()
                    row = pd.Series({'pubmed_accession_number':str(pubmed),'pmcid':pmcid})
                    dataframe = pd.concat([dataframe,row.to_frame().T],ignore_index=True)
                else:
                    row = pd.Series({'pubmed_accession_number':str(pubmed),'pmcid':None})
                    dataframe = pd.concat([dataframe,row.to_frame().T],ignore_index=True)
            dataframe.to_csv(save_in+'/pubmed_vs_pmcid.csv',index=False)
            browser.close()
