import requests
import os
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'https://www.ncbi.nlm.nih.gov'

def download_article_from_pmcid(pmcid: str, headless: bool = False, save_in: str = '.') -> None:
    '''
    Baixa um artigo do PMC usando um PMC ID e salva-o como um arquivo PDF.

    Parâmetros:
        - pmcid (str): PMC ID do artigo.
        - headless (bool): Indica se o navegador deve ser executado em modo headless.
        - save_in (str): Diretório para salvar o arquivo PDF.

    Retorna:
        - None
    '''
    full_url = f'{BASE_URL}/pmc/articles/{pmcid}'
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url=full_url)
        if page.get_by_role("link", name="PDF (").count() > 0:
            pdf_button = page.get_by_role("link", name="PDF (")
            link_for_request = BASE_URL + pdf_button.get_attribute('href')
            
            browser.close()
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url=link_for_request, headers=headers)
            response.raise_for_status()  # Verifica o status da resposta

            with open(os.path.join(save_in, f'{pmcid}.pdf'), 'wb') as file:
                file.write(response.content)

            print(f"Artigo {pmcid} baixado com sucesso.")
        else:
            print(f"Falha ao baixar o artigo {pmcid}. PDF não disponível.")
            with open(os.path.join(save_in, 'pmcid_não_baixados.txt'), 'a') as fail_file:
                fail_file.write(f'{pmcid}\n')

def download_articles_from_list_of_pmcid(list_of_pmcid: list[str], headless: bool, save_in: str = '.', max_workers: int = 1) -> None:
    '''
    Baixa artigos do PMC usando uma lista de PMC IDs em paralelo.

    Parâmetros:
        - list_of_pmcid (list[str]): Lista de PMC IDs dos artigos.
        - headless (bool): Indica se o navegador deve ser executado em modo headless.
        - save_in (str): Diretório para salvar os arquivos PDF.
        - max_workers (int): Número máximo de threads para execução em paralelo.

    Retorna:
        - None
    '''
    headless_flags = [headless] * len(list_of_pmcid)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(download_article_from_pmcid, list_of_pmcid, headless_flags, [save_in] * len(list_of_pmcid))