import os
import re
import requests
import xml.etree.ElementTree as ET
from ftplib import FTP
from logging import info, error
from urllib.parse import urlparse, unquote
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'https://www.ncbi.nlm.nih.gov'

def request_download_article_from_pmcid(pmcid: str, save_in: str = '.') -> bool:
    BASE_URL = 'https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi'
    params = {"id": pmcid}

    try:
        info(f"Efetuando requisição para o pmcid {pmcid}.")
        response = requests.get(url=BASE_URL, params=params)
        response.raise_for_status()
    except requests.RequestException as err:
        error(f"Erro ao executar a requisição do pmcid {pmcid} -> {err}")
        return False
    except Exception as err:
        error(f"Erro não mapeado ao efetuar a requisição do pmcid {pmcid} -> {err}")
        return False

    info("Verificando se há arquivo para baixar")
    root = ET.fromstring(response.content)
    if 'error' in [child.tag for child in root]:
        info("Baixar via requisição não funcionou, será usado webscraping.")
        return False

    info("Baixando via requisição no servidor FTP.")
    record = root.find("records").find("record")
    lastest_record = record.findall("link")[0].attrib
    ftp_url = lastest_record['href']
    ftp_format_file = lastest_record['format']

    info("Destrinchando a url recebida")
    parsed_url = urlparse(ftp_url)
    ftp_host = parsed_url.hostname
    ftp_path = parsed_url.path
    filename = unquote(ftp_path.split("/")[-1])
    filename_path = f'{save_in}/{ftp_format_file}/{filename}'

    info("Conectando ao servidor FTP")
    ftp = FTP(ftp_host)
    ftp.login()

    info("Baixando o arquivo")
    if not os.path.exists(f'{save_in}/{ftp_format_file}'):
        os.makedirs(f'{save_in}/{ftp_format_file}')

    try:
        with open(filename_path, 'wb') as file:
            ftp.retrbinary("RETR " + ftp_path, file.write)
    except Exception as err:
        error(f"Erro ao baixar ou salvar o arquivo -> {err}")
        return False
    finally:
        info("Saindo da conexão FTP")
        ftp.quit()

    return True

def webscraping_download_article_from_pmcid(pmcid: str, headless: bool = False, save_in: str = '.') -> None:
    '''
    Baixa um artigo do PMC usando um PMC ID e salva-o como um arquivo PDF.

    Parâmetros:
        - pmcid (str): PMC ID do artigo.
        - headless (bool): Indica se o navegador deve ser executado em modo headless.
        - save_in (str): Diretório para salvar o arquivo PDF.

    Retorna:
        - None
    '''
    try:
        full_url = f'{BASE_URL}/pmc/articles/{pmcid}'

        with sync_playwright() as p:
            browser = p.webkit.launch(headless=headless)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url=full_url, timeout=180000)

            pdf_links = page.locator("#main-content ul li a").filter(has_text="PDF")
            if pdf_links.count() > 0:
                link_for_request = BASE_URL + pdf_links.get_attribute('href')
                browser.close()

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url=link_for_request, headers=headers)
                response.raise_for_status()

                if not os.path.join(save_in,'pdf'):
                    os.makedirs(os.path.join(save_in,'pdf'))

                with open(os.path.join(save_in,'pdf', f'{pmcid}.pdf'), 'wb') as file:
                    file.write(response.content)

                info(f"Artigo {pmcid} baixado com sucesso.")
            else:
                info(f"Falha ao baixar o artigo {pmcid}. PDF não disponível.")
                with open(os.path.join(save_in + 'pdf', 'Artigos não baixados.txt'), 'a') as fail_file:
                    fail_file.write(f'(Sem link para download) {pmcid}\n')
    except Exception as err:
        error(f"Erro inesperado ao baixar o artigo {pmcid} -> {err}")
        with open(os.path.join(save_in, 'Artigos não baixados.txt'), 'a') as fail_request:
            fail_request.write(f'(Erro inesperado) {pmcid} - Erro: {err}\n')

        raise

def download_article_from_pmcid(pmcid: str, headless: bool = False, save_in: str = '.') -> None:

    try:
        if not request_download_article_from_pmcid(pmcid=pmcid, save_in=save_in):
            webscraping_download_article_from_pmcid(pmcid=pmcid,headless=headless,save_in=save_in)
    except Exception as err:
        error(f"Erro inesperado ao baixar o artigo (Usando ambos os métodos) {pmcid} -> {err}")
        with open(os.path.join(save_in, 'Artigos não baixados.txt'), 'a') as fail_request:
            fail_request.write(f'(Erro inesperado) {pmcid} - Erro: {err}\n')


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