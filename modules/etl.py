import pandas as pd
from modules.utilities import log, error
from concurrent.futures import ThreadPoolExecutor
from modules.download import download_article_from_pmcid
from modules.webScrapping import extract_pmcid_from_list

class Bronze:
    def __init__(self,data_path) -> None:
        '''
        '''
        self.data_path = data_path

    def __extract__(self):
        '''
        '''
        data_path = self.data_path

        log(msg=f"Lendo o arquivo csv {data_path}")
        data = pd.read_csv(data_path)
        return data

    def __transform__(self,dataframe:pd.DataFrame) -> pd.DataFrame:
        """
        Realiza o processamento de dados em um DataFrame, a partir de um caminho fornecido.

        Parâmetros:
        - data_path (str): Caminho do arquivo CSV contendo as colunas 'locus' e 'Pubmed Accession Number'.

        Retorna:
        - pd.DataFrame: DataFrame processado com a coluna 'pubmed_accession_number'.
        """
        
        # Transformando a string Pubmed accession number em uma lista
        log(msg="Transformando a string Pubmed accession number em uma lista")
        def transform_string_in_list(string):   # Função para transformar uma string em uma lista
            string = string.replace('[', '').replace(']', '').replace("'", '')
            lista = string.split(',')
            return lista
        dataframe['Pubmed accession number'] = dataframe['Pubmed accession number'].apply(transform_string_in_list)

        # Explode a coluna 'Pubmed accession number', transformando as listas em entradas individuais
        log(msg="Explodindo a coluna 'Pubmed accession number', transformando as listas em entradas individuais")
        dataframe_exploded = dataframe.explode('Pubmed accession number')

        # Remove linhas duplicadas no DataFrame resultante
        log(msg="Removendo linhas duplicadas no dataframe resultante")
        dataframe_exploded.drop_duplicates(inplace=True)

        # Aplica strip para remover espaços em branco
        log(msg="Tratando os espaços em branco no inicio e no fim")
        dataframe_exploded['Pubmed accession number'] = dataframe_exploded['Pubmed accession number'].apply(str.strip)

        log("Tratando o nome das colunas (minimizando e retirando espaços vazios)")
        dataframe_exploded.columns = [column.lower().replace(' ','_') for column in dataframe_exploded.columns]

        return dataframe_exploded

    def __load__(self, dataframe):
        '''
        '''

        log("Exportando os dados para data/processed/bronze.parquet")
        dataframe.to_parquet('data/processed/bronze.parquet',index=False)

    def full_process(self):
        '''
            Processo completo.
        '''

        # Extração
        dataframe = self.__extract__()
        
        # Transformação
        transformed_dataframe = self.__transform__(dataframe=dataframe)
        
        # Carregamento
        self.__load__(dataframe=transformed_dataframe)

class Silver:

    @staticmethod
    def __extract_():
        '''
        '''
        # Extração
        return pd.read_parquet('data/processed/bronze.parquet')
    
    @staticmethod
    def __transform__(bronze_df):
        '''
        '''
        # Transformação
        list_of_unique_pubmed = bronze_df['pubmed_accession_number'].unique()
        dict_of_pubmeds = extract_pmcid_from_list(list_of_pubmed=list_of_unique_pubmed,number_of_webscrappers=2)
        def extract_pmcid_list(dict_of_pubmeds:dict):
            list_of_pmcid = []
            for dictcionary in dict_of_pubmeds:
                pmcid = dictcionary.get('pmcid')
                if pmcid not in list_of_pmcid and pmcid is not None:
                    list_of_pmcid.append(pmcid)
            return list_of_pmcid
        
        list_of_pmcid = extract_pmcid_list(dict_of_pubmeds=dict_of_pubmeds)

        return list_of_pmcid
    
    @staticmethod
    def __load__(list_of_pmcid:list[str],max_workers:int=1):
        '''
        Baixa artigos do PMC usando uma lista de PMC IDs em paralelo.

        Parâmetros:
            - list_of_pmcid (list[str]): Lista de PMC IDs dos artigos.
            - max_workers (int): Número máximo de threads para execução em paralelo.

        Retorna:
            - None
        '''
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(download_article_from_pmcid, list_of_pmcid)

    @staticmethod
    def full_process():
        '''
        '''
        bronze_dataframe = Silver.__extract_()
        list_of_pmcid = Silver.__transform__(bronze_df=bronze_dataframe)
        Silver.__load__(list_of_pmcid=list_of_pmcid,max_workers=2)