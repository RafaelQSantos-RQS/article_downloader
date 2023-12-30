import pandas as pd

def data_processing(data_path: str, save_in: str = None) -> pd.DataFrame:
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
    data = pd.read_csv(data_path)

    # Função para transformar uma string em uma lista
    def transform_string_in_list(string):
        string = string.replace('[', '').replace(']', '').replace("'", '')
        lista = string.split(',')
        return lista

    # Aplica a função à coluna 'Pubmed accession number'
    data['Pubmed accession number'] = data['Pubmed accession number'].apply(transform_string_in_list)

    # Explode a coluna 'Pubmed accession number', transformando as listas em entradas individuais
    data_exploded = data.explode('Pubmed accession number')

    # Remove linhas duplicadas no DataFrame resultante
    data_exploded.drop_duplicates(inplace=True)

    # Aplica strip para remover espaços em branco
    data_exploded['Pubmed accession number'] = data_exploded['Pubmed accession number'].apply(str.strip)

    # Salva o DataFrame processado como um arquivo CSV, se um caminho for fornecido
    if save_in is not None:
        data_exploded.to_csv(save_in, index=False)
        return None
    else:
        return data_exploded