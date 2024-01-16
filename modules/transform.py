import pandas as pd
from typing import Optional
from logging import info, error, INFO, basicConfig

basicConfig(level=INFO, format=f'%(asctime)s (%(funcName)s): %(message)s',datefmt='%d/%m/%Y %H:%M:%S')

def data_processing(data_path: str, save_in: str = None) -> Optional[pd.DataFrame]:
    """
    Realiza o processamento de dados em um DataFrame, a partir de um caminho fornecido.

    Parâmetros:
    - data_path (str): Caminho do arquivo CSV contendo as colunas 'locus' e 'Pubmed Accession Number'.
    - save_in (str): Caminho para salvar o DataFrame processado como um arquivo CSV. Se None, o DataFrame é retornado.

    Retorna:
    - pd.DataFrame: DataFrame processado com a coluna 'pubmed_accession_number'.

    Exemplo de uso:
    >>> df_resultado = data_processing('caminho/do/arquivo.csv', save_in='caminho/do/arquivo/processado.csv')
    """

    # Lê o arquivo CSV fornecido
    info(msg=f"Lendo o arquivo csv {data_path}")
    data = pd.read_csv(data_path)

    
    # Transformando a string Pubmed accession number em uma lista
    info(msg="Transformando a string Pubmed accession number em uma lista")
    def transform_string_in_list(string):   # Função para transformar uma string em uma lista
        string = string.replace('[', '').replace(']', '').replace("'", '')
        lista = string.split(',')
        return lista
    data['Pubmed accession number'] = data['Pubmed accession number'].apply(transform_string_in_list)

    # Explode a coluna 'Pubmed accession number', transformando as listas em entradas individuais
    info(msg="Explodindo a coluna 'Pubmed accession number', transformando as listas em entradas individuais")
    data_exploded = data.explode('Pubmed accession number')

    # Remove linhas duplicadas no DataFrame resultante
    info(msg="Removendo linhas duplicadas no dataframe resultante")
    data_exploded.drop_duplicates(inplace=True)

    # Aplica strip para remover espaços em branco
    info(msg="Tratando os espaços em branco no inicio e no fim")
    data_exploded['Pubmed accession number'] = data_exploded['Pubmed accession number'].apply(str.strip)

    # Salva o DataFrame processado como um arquivo CSV, se um caminho for fornecido
    if save_in is not None:
        info(msg=f"Salvando o dataframe em {save_in}")
        data_exploded.to_csv(save_in, index=False)
        return None
    else:
        info(msg=f"Retornando o dataframe resultante")
        return data_exploded