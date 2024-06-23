import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from modules.utilities import log, error
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'https://pubmed.ncbi.nlm.nih.gov'
def extract_pcmid_from_pubmed(pubmed:str) -> dict:
    """
    Extrai o PMCID (PubMed Central ID) associado a um número de acesso do PubMed.

    Parâmetros:
    - pubmed (str): O número de acesso do PubMed.

    Retorna:
    - dict: Um dicionário contendo as informações, incluindo o número de acesso do PubMed e o PMCID.

    Exceções:
    - requests.HTTPError: Caso ocorra um erro HTTP ao fazer a requisição à URL.
    - Exception: Para outros erros inesperados durante a execução.

    Exemplo:
    ```python
    result = extract_pcmid_from_pubmed('12345678')
    # Saída esperada: {'pubmed_accession_number': '12345678', 'pmcid': 'PMC1234567'}
    ```

    OBSERVAÇÃO:
    - A função acessa a página do PubMed correspondente ao número de acesso fornecido.
    - Extrai o PMCID da página, se disponível.
    - Retorna um dicionário com informações sobre o número de acesso do PubMed e o PMCID.
    - Se o PMCID não estiver disponível, será retornado como `None`.
    - Caso ocorram erros durante a requisição ou análise da página, exceções são levantadas.
    """
    url = f'{BASE_URL}/{pubmed}'
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content,"html.parser")
        tag = soup.find(attrs={"data-ga-action": "PMCID"})
        if tag:
            pmcid = tag.text.strip()
        else:
            pmcid = None
        result = {'pubmed_accession_number': str(pubmed), 'pmcid': pmcid}
        log(msg=f'Pubmed: {result.get("pubmed_accession_number")} -> PMCID: {result.get("pmcid")}')
        return result
    except requests.RequestException as err:
        error(f"Erro ao fazer requisição a url ({url}) -> {err}")
        raise err
    except Exception as err:
        error(f"Erro inesperado -> {err}")
        raise err
        

def extract_pmcid_from_list(list_of_pubmed: list[str], number_of_webscrappers: int = 1) -> dict:
    '''
    Extrai informações de PMCID para uma lista de números Pubmed em paralelo usando ThreadPoolExecutor.
    Os resultados são armazenados em um DataFrame e exportados para um arquivo CSV.

    Parâmetros:
        - list_of_pubmed (List[str]): Lista de números Pubmed.
        - number_of_webscrappers (int): Número de processos paralelos.

    Retorna:
        - None
    '''    
    with ThreadPoolExecutor(max_workers=number_of_webscrappers) as executor:
        results = list(executor.map(extract_pcmid_from_pubmed, list_of_pubmed))

    return results
