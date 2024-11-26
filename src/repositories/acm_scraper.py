from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def fetch_acm_search_results(search_variable):
    base_url = "https://dl.acm.org/action/doSearch?"
    query_params = {"AllField": search_variable}
    encoded_query = urlencode(query_params)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    search_url = f"{base_url}{encoded_query}"
    driver.get(search_url)

    wait = WebDriverWait(driver, 20)
    try:
        results_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-result__xsl-body")))
    except:
        driver.quit()
        return None

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    first_result = soup.find('li', class_='search__item')
    if not first_result:
        driver.quit()
        return None

    title_tag = first_result.find('h5', class_='issue-item__title')
    title = title_tag.text.strip() if title_tag else "Title ei löytynyt"

    author_list = first_result.find('ul', class_='rlist--inline loa truncate-list')
    authors = ', '.join(
        author.find('span').text.strip() for author in author_list.find_all('li') if author.find('span')
    ) if author_list else "Authoreita ei löytynyt"

    year_tag = first_result.find('div', class_='bookPubDate')
    year = None
    if year_tag:
        year = year_tag.text.strip().split()[-1]
    year = year if year else "Vuotta ei löytynyt"

    doi_link = None
    if title_tag:
        link_tag = title_tag.find('a')
        if link_tag and 'href' in link_tag.attrs:
            doi_link = f"https://dl.acm.org{link_tag['href']}"
    doi_link = doi_link if doi_link else "DOI-linkkiä ei löytynyt"

    result_data = {
        "title": title,
        "authors": authors,
        "year": year,
        "doi_link": doi_link
    }

    driver.quit()
    return result_data