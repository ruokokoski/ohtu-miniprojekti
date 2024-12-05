import time
from urllib.parse import urlencode
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

def fetch_search_results(database, search_variable):
    if database == "ACM":
        return fetch_acm_search_results(search_variable)
    if database == "Google Scholar":
        return fetch_google_scholar_results(search_variable)
    raise ValueError(f"Database {database} not supported.")

def fetch_google_scholar_results(search_variable):
    driver = initialize_webdriver()
    search_url = "https://scholar.google.com/"
    driver.get(search_url)

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(search_variable)
        search_box.submit()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gs_res_ccl_mid"))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        results = []
        for item in soup.find_all('div', class_='gs_r gs_or gs_scl'):
            title_tag = item.find('h3', class_='gs_rt')
            title = title_tag.text.strip() if title_tag else "-"
            if title_tag and title_tag.find('a'):
                link = title_tag.find('a')['href']
            else:
                link = "Link not available"
            title = title.replace("[HTML]", "")
            title = title.replace("[PDF]", "")
            title = title.replace("[CITATION]", "")
            title = title.replace("[BOOK]", "").replace("[B]", "")
            title = title.strip()

            author_year_tag = item.find('div', class_='gs_a')
            #author_year_text = author_year_tag.text.strip() if author_year_tag else "-"
            authors, year = parse_author_year(
                author_year_tag.text.strip() if item.find('div', class_='gs_a') else "-"
            )

            result = {
                "title": title,
                "authors": authors,
                "year": year,
                "doi_link": link,
                "pdf_url": "Not available"
            }
            results.append(result)

    except (TimeoutException, WebDriverException):
        results = None
    finally:
        driver.quit()

    return results

def parse_author_year(author_year_text):
    if author_year_text == "-":
        return "n.d.", "-"

    parts = author_year_text.split('-')
    authors = parts[0].strip() if len(parts) > 0 else "n.d."
    year = parts[-2].strip()[-4:] if len(parts) > 1 and parts[-2].strip()[-4:].isdigit() else "-"
    return authors, year

def fetch_acm_search_results(search_variable):
    driver = initialize_webdriver()
    search_url = build_search_url(search_variable)
    driver.get(search_url)

    soup = load_page_and_get_soup(driver)
    if not soup:
        return None

    time.sleep(3)
    results = get_results(soup, 10) # kuinka monta listataan
    if not results:
        driver.quit()
        return None

    #debug:
    #print(f"Fetched HTML: {driver.page_source}")
    #print(f"Fetched Results: {results}")

    result_data_list = [process_result(result, index) for index, result in enumerate(results)]

    return result_data_list

def process_result(result, index):
    title, title_tag = get_title(result)
    year = get_year(result)
    doi_link, pdf_url = get_doi_link(title_tag)
    authors = get_authors(result)
    bibtex = fetch_bibtex(doi_link)

    return {
        "result_id": index,
        "title": title,
        "authors": authors,
        "year": year,
        "doi_link": doi_link,
        "pdf_url": pdf_url,
        "bibtex": bibtex,
    }

def fetch_bibtex(doi_link):
    doi = doi_link.rsplit('https://dl.acm.org/doi/', maxsplit=1)[-1]
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        print(f"Failed to fetch BibTeX for DOI {doi}. ")
        return None
    except requests.RequestException as e:
        print(f"Error fetching BibTeX for DOI {doi}: {e}")
        return None

def initialize_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)

def build_search_url(search_variable):
    base_url = "https://dl.acm.org/action/doSearch?"
    query_params = {"AllField": search_variable}
    return f"{base_url}{urlencode(query_params)}"

def load_page_and_get_soup(driver):
    wait = WebDriverWait(driver, 15)
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
    results = soup.find_all('li', class_='search__item')
    if len(results) > 5:
        results.pop(5)  # Poista 6., joka on mainos

    return results[:count]

def get_authors(result):
    author_list = result.find('ul', class_='rlist--inline loa truncate-list')
    if author_list:
        authors = ', '.join(
            author.find('span').text.strip()
            for author in author_list.find_all('li')
            if author.find('span')
        )
    else:
        authors = "n.d."
    return authors

def get_title(result):
    title_tag = result.find('h5', class_='issue-item__title')
    title = title_tag.text.strip() if title_tag else "-"
    return title, title_tag

def get_year(result):
    year_tag = result.find('div', class_='bookPubDate')
    year = None
    if year_tag:
        year = year_tag.text.strip().split()[-1]
    year = year if year else "-"
    return year

def get_doi_link(title_tag):
    doi_link = None
    pdf_url = None
    if title_tag:
        link_tag = title_tag.find('a')
        if link_tag and 'href' in link_tag.attrs:
            doi_path = link_tag['href']
            doi_link = f"https://dl.acm.org{doi_path}"
            pdf_url = f"https://dl.acm.org/doi/pdf{doi_path.split('/doi')[-1]}"
    doi_link = doi_link if doi_link else "DOI-link not found"
    pdf_url = pdf_url if pdf_url else "PDF-link not found"
    return doi_link, pdf_url
