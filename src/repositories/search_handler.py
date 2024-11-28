import time
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

def fetch_acm_search_results(search_variable):
    driver = initialize_webdriver()
    search_url = build_search_url(search_variable)
    driver.get(search_url)

    soup = load_page_and_get_soup(driver)
    if not soup:
        return None

    time.sleep(3)
    results = get_results(soup, 5)
    if not results:
        driver.quit()
        return None

    result_data_list = []
    for result in results:
        title, title_tag = get_title(result)
        year = get_year(result)
        doi_link = get_doi_link(title_tag)
        authors = get_authors(result)

        result_data = {
            "title": title,
            "authors": authors,
            "year": year,
            "doi_link": doi_link
        }
        result_data_list.append(result_data)

    driver.quit()
    return result_data_list

def initialize_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)

def build_search_url(search_variable):
    base_url = "https://dl.acm.org/action/doSearch?"
    query_params = {"AllField": search_variable}
    return f"{base_url}{urlencode(query_params)}"

def load_page_and_get_soup(driver):
    wait = WebDriverWait(driver, 20)
    try:
        # results_containeria tarvitaan myöhemmin bibtex-buttonin hakua varten
        # pylint: disable=unused-variable
        results_container = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "search-result__xsl-body")
            )
        )
        html = driver.page_source
        return BeautifulSoup(html, 'html.parser')
    except (TimeoutException, WebDriverException):
        driver.quit()
        return None

def get_results(soup, count):
    return soup.find_all('li', class_='search__item', limit=count)

def get_authors(result):
    author_list = result.find('ul', class_='rlist--inline loa truncate-list')
    if author_list:
        authors = ', '.join(
            author.find('span').text.strip()
            for author in author_list.find_all('li')
            if author.find('span')
        )
    else:
        authors = "--"
    return authors

def get_title(result):
    title_tag = result.find('h5', class_='issue-item__title')
    title = title_tag.text.strip() if title_tag else "--"
    return title, title_tag

def get_year(result):
    year_tag = result.find('div', class_='bookPubDate')
    year = None
    if year_tag:
        year = year_tag.text.strip().split()[-1]
    year = year if year else "Vuotta ei löytynyt"
    return year

def get_doi_link(title_tag):
    doi_link = None
    if title_tag:
        link_tag = title_tag.find('a')
        if link_tag and 'href' in link_tag.attrs:
            doi_link = f"https://dl.acm.org{link_tag['href']}"
    doi_link = doi_link if doi_link else "DOI-linkkiä ei löytynyt"
    return doi_link
