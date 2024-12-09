import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from repositories.search_handler import (
    fetch_search_results,
    initialize_webdriver,
    build_search_url,
    get_results,
    get_authors,
    get_title,
    get_year,
    get_doi_link,
)


class TestFetchSearchResults(unittest.TestCase):
    @patch("repositories.search_handler.webdriver.Chrome")
    def test_fetch_google_scholar_results(self, mock_webdriver):
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver

        mock_driver.page_source = """
        <div id="gs_res_ccl_mid">
            <div class="gs_r gs_or gs_scl">
                <h3 class="gs_rt"><a href="https://example.fi">Example Title</a></h3>
                <div class="gs_a">Author1, Author2 - 2024 - Proceedings</div>
            </div>
        </div>
        """
        mock_driver.get.return_value = None

        results = fetch_search_results("Google Scholar", "test query")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Example Title")
        self.assertEqual(results[0]['authors'], "Author1, Author2")
        self.assertEqual(results[0]['year'], "2024")
        self.assertEqual(results[0]['doi_link'], "https://example.fi")

        mock_driver.quit.assert_called_once()

    @patch("repositories.search_handler.webdriver.Chrome")
    def test_initialize_webdriver(self, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        driver = initialize_webdriver(headless=True)

        mock_chrome.assert_called_once()
        mock_driver.set_window_size.assert_not_called()
        self.assertIsNotNone(driver)
        driver.quit()

    def test_build_search_url(self):
        search_variable = "test query"
        expected_url = f"https://dl.acm.org/action/doSearch?{urlencode({'AllField': search_variable})}"

        result_url = build_search_url(search_variable)

        self.assertEqual(result_url, expected_url)

    def test_get_authors(self):
        html = """
        <ul class="rlist--inline loa truncate-list">
            <li><span>Author1</span></li>
            <li><span>Author2</span></li>
        </ul>
        """
        result = BeautifulSoup(html, "html.parser")
        self.assertEqual(get_authors(result), "Author1, Author2")

        html = """<div></div>"""
        result = BeautifulSoup(html, "html.parser")
        self.assertEqual(get_authors(result), "n.d.")

    def test_get_title(self):
        html = """
        <h5 class="issue-item__title">
            Example Title
        </h5>
        """
        result = BeautifulSoup(html, "html.parser")
        title, title_tag = get_title(result)
        self.assertEqual(title, "Example Title")
        self.assertIsNotNone(title_tag)

        html = """<div></div>"""
        result = BeautifulSoup(html, "html.parser")
        title, title_tag = get_title(result)
        self.assertEqual(title, "-")
        self.assertIsNone(title_tag)

    def test_get_year(self):
        html = """
        <div class="bookPubDate">Published: January 2024</div>
        """
        result = BeautifulSoup(html, "html.parser")
        self.assertEqual(get_year(result), "2024")

        html = """<div></div>"""
        result = BeautifulSoup(html, "html.parser")
        self.assertEqual(get_year(result), "-")

    def test_get_doi_link(self):
        html = """
        <h5 class="issue-item__title">
            <a href="/doi/10.1145/example">Example Title</a>
        </h5>
        """
        result = BeautifulSoup(html, "html.parser").find('h5', class_='issue-item__title')
        doi_link, pdf_url = get_doi_link(result)
        self.assertEqual(doi_link, "https://dl.acm.org/doi/10.1145/example")
        self.assertEqual(pdf_url, "https://dl.acm.org/doi/pdf/10.1145/example")

        html = """<h5 class="issue-item__title"></h5>"""
        result = BeautifulSoup(html, "html.parser").find('h5', class_='issue-item__title')
        doi_link, pdf_url = get_doi_link(result)
        self.assertEqual(doi_link, "DOI-link not found")
        self.assertEqual(pdf_url, "PDF-link not found")
    
    def test_get_results(self):
        html = """
        <ul>
            <li class="search__item">Result 1</li>
            <li class="search__item">Result 2</li>
            <li class="search__item">Result 3</li>
            <li class="search__item">Result 4</li>
            <li class="search__item">Result 5</li>
            <li class="search__item">Result 6 (ad)</li>
        </ul>
        """
        soup = BeautifulSoup(html, "html.parser")
        results = get_results(soup, 5)

        self.assertEqual(len(results), 5)
        self.assertEqual(results[4].text.strip(), "Result 5")
        
        self.assertNotIn("Result 6 (ad)", [result.text.strip() for result in results])

        html = """
        <ul>
            <li class="search__item">Result 1</li>
            <li class="search__item">Result 2</li>
            <li class="search__item">Result 3</li>
            <li class="search__item">Result 4</li>
            <li class="search__item">Result 5</li>
        </ul>
        """
        soup = BeautifulSoup(html, "html.parser")
        results = get_results(soup, 5)

        self.assertEqual(len(results), 5)

        html = """
        <ul>
            <li class="search__item">Result 1</li>
            <li class="search__item">Result 2</li>
        </ul>
        """
        soup = BeautifulSoup(html, "html.parser")
        results = get_results(soup, 5)

        self.assertEqual(len(results), 2)