from playwright.sync_api import sync_playwright
import requests

BASE_URL = 'https://www.ncbi.nlm.nih.gov'

def download_article_from_pmcid(pmcid:str,save_in:str='.'):
    '''
    '''
    full_url = f'{BASE_URL}/pmc/articles/{pmcid}'
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url=full_url)
        pdf_button = page.get_by_role("link", name="PDF (")
        link_for_request = BASE_URL + pdf_button.get_attribute('href')
        browser.close()
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url=link_for_request,headers=headers)
        with open(f'{save_in}/{pmcid}.pdf','wb') as file:
            file.write(response.content)
        print(response.headers.get('Content-Type'))
