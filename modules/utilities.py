import os

class Utilities:
    '''
    '''
    @staticmethod
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
        list_of_path = ['data/raw', 'data/processed']

        # Loop pelos caminhos e tenta criar os diretórios
        for path in list_of_path:
            try:
                os.makedirs(path)
                print(f"O diretório {path} foi criado com sucesso.")
            except FileExistsError:
                print(f"O diretório {path} já existe!")
            except Exception as err:
                print(f"Erro ao criar o diretório {path}: {err}")