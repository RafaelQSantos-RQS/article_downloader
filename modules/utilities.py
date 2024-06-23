import os
from datetime import datetime

def datetimestamp():
    return datetime.now().strftime('[%d/%m/%Y %H:%M:%S]')

def log(msg):
    print('[LOG]',datetimestamp(),msg)
    
def error(msg):
        print('[ERROR]',datetimestamp(),msg)

def setup_filesystem():
    '''
    Description
    -----------
        Configura o sistema de arquivos criando diretórios para armazenar dados brutos e processados.

    Parameters
    ----------
        None.
    
    Return
    ------
        None.

    '''
    # Lista de caminhos dos diretórios a serem criados
    list_of_path = ['data/raw', 'data/processed','data/articles/pdf','data/articles/tgz']
    # Loop pelos caminhos e tenta criar os diretórios
    for path in list_of_path:
        try:
            os.makedirs(path)
            log(f"O diretório {path} foi criado com sucesso.")
        except FileExistsError:
            error(f"O diretório {path} já existe!")
        except Exception as err:
            error(f"Erro ao criar o diretório {path}: {err}")