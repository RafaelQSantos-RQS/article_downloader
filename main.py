from modules.etl import Bronze, Silver
from modules.utilities import setup_filesystem


def main():
    print("## PREPARAÇÃO DO SISTEMA DE ARQUIVOS ##")
    setup_filesystem()

    print("## BRONZE ##")
    bronze_step = Bronze(data_path='data/raw/DENV2_locus_pubmed.csv')
    bronze_step.full_process()

    print("## SILVER ##")
    Silver.full_process()



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e