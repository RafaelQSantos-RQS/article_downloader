# Article downloader
## Cenário
Este projeto envolve a criação de uma solução de automação, na qual desenvolvi uma abordagem para manipular um [conjunto de dados](data/raw/DENV2_locus_pubmed.csv) contendo duas colunas, denominadas **locus** e **Pubmed Accession Number**. O processo abrange três macros etapas: tratamento dos dados, extração dos identificadores PMC (PubMed Central) correspondentes aos números de acesso do Pubmed e o download dos artigos associados aos identificadores PMC.

# Funcionalidades
## 1. Extração de PMCID a partir de um pubmed (extract_pcmid_from_pubmed)
Esta função solicita ao usuário um identificador pubmed e através de uma automação web o bot acessa o site do [pubmed](https://pubmed.ncbi.nlm.nih.gov) e extrai o PMCID associado, caso tenha.
## 2. Extracção de uma lista de PMCIDs a partir de uma lista de pubmeds (extract_pmcid_from_list)
Nesta função usuário deve fornecer uma lista sem valores vazios de identificadores pubmed e através de uma automação web o bot acessa o site do [pubmed](https://pubmed.ncbi.nlm.nih.gov) e extrai o PMCID associado, em seguida os salva em um arquivo csv.

**Obs.:** é possível escolher a quantidade de scrappers que atuarão nessa demanda, pois através de mult thread, pode-se executar vários scrapper ao mesmo tempo, contudo cuidado com esta função pois depende da máquina em que está sendo executado.
## 3. Download de artigo a partir de um PMCID (download_article_from_pmcid)
Nesta função o usuário deve fornecer um PMCID e a automação acessa o PubMed Central, verifica a disponilidade do PDF e realiza o download dos artigos, caso o artigo não esteja disponível um txt será criado informando o PMCID não disponível.
## 4. Download de artigos a partir de uma lista de PMCIDs (download_articles_from_list_of_pmcid)
Nesta função o usuário deve fornecer uma lista de PMCID, que não tenha valores NaN e a automação acessa o PubMed Central, verifica a disponilidade do PDF e realiza o download dos artigos, caso o artigo não esteja disponível um txt será criado informando o PMCID não disponível.

# Requisitos
- Python 3.10.12 ou mais.
- Bibliotecas necessários (Consultar [Requerimentos](requirements.txt))

Este projeto visa simplificar o processo de pesquisa e obtenção de artigos científicos, proporcionando uma automação eficiente para a extração de PMCIDs e o download dos artigos correspondentes.