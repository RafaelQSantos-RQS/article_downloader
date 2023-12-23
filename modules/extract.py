import pandas as pd
import os
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'https://pubmed.ncbi.nlm.nih.gov'

def extract_pcmid_from_pubmed(pubmed:str,headless:bool=False) -> dict:
    '''
    Extrai o PMCID associado a um número Pubmed específico.

    Parâmetros:
        - pubmed (str): Número Pubmed.

    Retorna:
        - dict: Dicionário contendo 'pubmed_accession_number' e 'pmcid'.
    '''
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        url = f'{BASE_URL}/{pubmed}'
        page.goto(url=url,timeout=240000)
        if page.locator("#full-view-identifiers li").filter(has_text="PMCID").count() > 0:
            pmcid = page.locator("#full-view-identifiers li").filter(has_text="PMCID").inner_text().replace('PMCID: ','').strip()
            result =  {'pubmed_accession_number': str(pubmed), 'pmcid': pmcid}
        else:
            result = {'pubmed_accession_number': str(pubmed), 'pmcid': None}
        
        browser.close()

        return result

def extract_pmcid_from_list(list_of_pubmed: list[str], number_of_webscrappers: int = 1,headless: bool = False, save_in: str = '.') -> None:
    '''
    Extrai informações de PMCID para uma lista de números Pubmed em paralelo usando ThreadPoolExecutor.
    Os resultados são armazenados em um DataFrame e exportados para um arquivo CSV.

    Parâmetros:
        - list_of_pubmed (List[str]): Lista de números Pubmed.
        - number_of_webscrappers (int): Número de processos paralelos.
        - save_in (str): Diretório para salvar o arquivo CSV resultante.

    Retorna:
        - None
    '''
    dataframe = pd.DataFrame(columns=['pubmed_accession_number', 'pmcid'])
    headless_flags = [headless] * len(list_of_pubmed)
    
    with ThreadPoolExecutor(max_workers=number_of_webscrappers) as executor:
        results = list(executor.map(extract_pcmid_from_pubmed, list_of_pubmed, headless_flags))

    for result in results:
        row = pd.Series(result)
        dataframe = pd.concat([dataframe, row.to_frame().T], ignore_index=True)
    
    csv_path = os.path.join(save_in, 'pubmed_vs_pmcid.csv')
    dataframe.to_csv(csv_path, index=False)
    print(f"Resultados salvos em: {csv_path}")
