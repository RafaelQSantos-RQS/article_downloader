import os
from datetime import datetime
from logging import info

def setup_filesystem():
    '''
    Configura o sistema de arquivos criando diretórios para armazenar dados brutos e processados.

    Parameters
    ----------
        None.
    
    Return
    ------
        None.

    '''
    # Lista de caminhos dos diretórios a serem criados
    list_of_path = ['data/raw', 'data/processed','data/downloaded/pdf','data/downloaded/tgz']
    # Loop pelos caminhos e tenta criar os diretórios
    for path in list_of_path:
        try:
            os.makedirs(path)
            info(f"O diretório {path} foi criado com sucesso.")
        except FileExistsError:
            info(f"O diretório {path} já existe!")
        except Exception as err:
            info(f"Erro ao criar o diretório {path}: {err}")
        
def datetimestamp():
    return datetime.now().strftime('%d/%m/%Y - %H:%M:%S')