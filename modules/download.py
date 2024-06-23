import os
import requests
from ftplib import FTP
from bs4 import BeautifulSoup
from modules.utilities import log, error
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote

def request_download_article_from_pmcid(pmcid: str, save_in: str = '.') -> bool:
    BASE_URL = 'https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi'
    params = {"id": pmcid}

    try:
        log(f"Efetuando requisição para o pmcid {pmcid}.")
        response = requests.get(url=BASE_URL, params=params)
        response.raise_for_status()
    except requests.RequestException as err:
        error(f"Erro ao executar a requisição do pmcid {pmcid} -> {err}")
        return False
    except Exception as err:
        error(f"Erro não mapeado ao efetuar a requisição do pmcid {pmcid} -> {err}")
        return False

    log("Verificando se há arquivo para baixar")
    root = ET.fromstring(response.content)
    if 'error' in [child.tag for child in root]:
        log("Baixar via requisição não funcionou, será usado webscraping.")
        return False

    log("Baixando via requisição no servidor FTP.")
    record = root.find("records").find("record")
    lastest_record = record.findall("link")[0].attrib
    ftp_url = lastest_record['href']
    ftp_format_file = lastest_record['format']

    log("Destrinchando a url recebida")
    parsed_url = urlparse(ftp_url)
    ftp_host = parsed_url.hostname
    ftp_path = parsed_url.path
    filename = unquote(ftp_path.split("/")[-1])
    filename_path = f'{save_in}/{ftp_format_file}/{filename}'

    log("Conectando ao servidor FTP")
    ftp = FTP(ftp_host)
    ftp.login()

    log("Baixando o arquivo")
    os.makedirs(f'{save_in}/{ftp_format_file}',exist_ok=True)

    try:
        with open(filename_path, 'wb') as file:
            ftp.retrbinary("RETR " + ftp_path, file.write)
    except Exception as err:
        error(f"Erro ao baixar ou salvar o arquivo -> {err}")
        raise err
    finally:
        log("Saindo da conexão FTP")
        ftp.quit()

def webscraping_download_article_from_pmcid(pmcid: str) -> None:
    '''
    Baixa um artigo do PMC usando um PMC ID e salva-o como um arquivo PDF.

    Parâmetros:
        - pmcid (str): PMC ID do artigo.
        - headless (bool): Indica se o navegador deve ser executado em modo headless.
        - save_in (str): Diretório para salvar o arquivo PDF.

    Retorna:
        - None
    '''
    # Diretório para salvar os PDFs
    output_dir = 'data/articles/pdf/'
    log(f"Criando o diretório {output_dir}, caso não exista.")
    os.makedirs(output_dir, exist_ok=True)

    # Cabeçalhos para a requisição
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        url = f'https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/'
        log("Efetuando a requisição")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        log("Iniciando a raspagem de dados")
        soup = BeautifulSoup(response.content, 'html.parser')
        pdf_element = soup.find(class_='pdf-link other_item').find(class_='int-view')

        log("Efetuando a requisição para o link de download")
        download_url = 'https://www.ncbi.nlm.nih.gov' + pdf_element['href']
        pdf_response = requests.get(download_url, headers=headers)
        pdf_response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        with open(f'{output_dir}/{pmcid}.pdf', 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)
        log(f'Successfully downloaded {pmcid}.pdf')

    except requests.exceptions.RequestException as e:
        error(f'Failed to download {pmcid}: {e}')
        raise e
    
    except Exception as e:
        error(f'An error occurred for {pmcid}: {e}')
        raise e

def download_article_from_pmcid(pmcid: str) -> None:
    """
    Tenta baixar um artigo do PMC usando dois métodos diferentes: web scraping e requisições HTTP diretas.

    O método primeiro tenta baixar o artigo via web scraping. Se falhar, tenta baixar via requisição HTTP direta.
    Se ambos os métodos falharem, o erro é registrado e o PMC ID é salvo em um arquivo de log.

    Args:
        pmcid (str): O ID do artigo no PubMed Central (PMC) a ser baixado.

    Raises:
        Exception: Propaga a exceção se ambos os métodos falharem.
    """
    try:
        # Primeiro método: webscraping
        try:
            webscraping_download_article_from_pmcid(pmcid=pmcid)
        except Exception as e:
            error(f"Erro ao baixar o artigo via webscraping {pmcid} -> {e}")
            # Segundo método: request
            try:
                request_download_article_from_pmcid(pmcid=pmcid, save_in='./data/articles')
            except Exception as e:
                error(f"Erro ao baixar o artigo via request {pmcid} -> {e}")
                raise e
    except Exception as err:
        error(f"Erro inesperado ao baixar o artigo (usando ambos os métodos) {pmcid} -> {err}")
        with open(os.path.join('data/', 'Artigos_nao_baixados.txt'), 'a') as fail_request:
            fail_request.write(f'(Erro inesperado) {pmcid} - Erro: {err}\n')