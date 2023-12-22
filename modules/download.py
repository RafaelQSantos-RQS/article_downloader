from playwright.sync_api import sync_playwright

BASE_URL = 'https://www.ncbi.nlm.nih.gov'

def download_article_from_pmcid(pmcid:str,save_in:str='./'):
    '''
    '''
    full_url = f'{BASE_URL}/pmc/articles/{pmcid}'
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False,downloads_path='data/raw/articles')
        context = browser.new_context()
        page = context.new_page()
        page.goto(url=full_url)
        pdf_button = page.get_by_role("link", name="PDF (")
        new_url = BASE_URL + pdf_button.get_attribute('href')
        with page.goto(url=new_url).expect_download() as download_info:
            
        download = download_info.value

        download.save_as(save_in + pmcid)
        browser.close()
