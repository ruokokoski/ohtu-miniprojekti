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
    check_pdf,
    search_specific,
    get_sch_bibtex,
    fetch_helka_results,
    build_helka_url,
    parse_results,
    extract_result_data,
    extract_year,
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

    def test_check_pdf(self):
        acm_link = "https://dl.acm.org/doi/10.1145/example"
        pdf_url = check_pdf(acm_link)
        expected_pdf_url = "https://dl.acm.org/doi/pdf/10.1145/example"
        self.assertEqual(pdf_url, expected_pdf_url)

        non_acm_link = "https://example.com/some-article"
        pdf_url = check_pdf(non_acm_link)
        self.assertIsNone(pdf_url)

    @patch("repositories.search_handler.initialize_webdriver")
    def test_search_specific(self, mock_initialize_webdriver):
        mock_driver = MagicMock()
        mock_initialize_webdriver.return_value = mock_driver
        
        mock_driver.get.return_value = None
        mock_driver.quit.return_value = None
        
        with patch("repositories.search_handler.get_sch_bibtex") as mock_get_sch_bibtex:
            mock_get_sch_bibtex.return_value = "@article{example, title={Example Title}}"
            bibtex = search_specific("Example Title")
            
            mock_driver.get.assert_called_once_with("https://scholar.google.com/scholar?q=Example+Title&num=1")
            self.assertEqual(bibtex, "@article{example, title={Example Title}}")

    @patch("repositories.search_handler.WebDriverWait")
    def test_get_sch_bibtex(self, mock_webdriver_wait):
        mock_driver = MagicMock()
        
        mock_cite_button = MagicMock()
        mock_cite_button.click.return_value = None
        
        mock_bibtex_button = MagicMock()
        mock_bibtex_button.click.return_value = None
        
        mock_bibtex_content = MagicMock()
        mock_bibtex_content.text = "@article{example, title={Example Title}}"
        
        mock_webdriver_wait.return_value.until.side_effect = [
            mock_cite_button,
            None,
            mock_bibtex_button,
            mock_bibtex_content
        ]
        
        bibtex = get_sch_bibtex(mock_driver)
        self.assertEqual(bibtex, "@article{example, title={Example Title}}")

    @patch("repositories.search_handler.initialize_webdriver")
    def test_fetch_helka_results_success(self, mock_initialize_webdriver):
        mock_driver = MagicMock()
        mock_initialize_webdriver.return_value = mock_driver

        mock_driver.page_source = """
        <div class="list-item-wrapper">
            <h3>Test Title / Test Author</h3>
            <a ng-href="https://example.com"></a>
            <div></div><div><span ng-if="::(!$ctrl.isEmailMode())">2024</span></div>
        </div>
        """
        mock_driver.get.return_value = None

        with patch("repositories.search_handler.generate_human_like_delay"):
            results = fetch_helka_results("test query")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Test Title ")
        self.assertEqual(results[0]["authors"], "Test Author")
        self.assertEqual(results[0]["year"], "2024")
        self.assertEqual(results[0]["doi_link"], "https://example.com")

        mock_driver.quit.assert_called_once()

    def test_build_helka_url(self):
        search_variable = "test query"
        expected_url = (
            "https://helka.helsinki.fi/discovery/search?vid=358UOH_INST:VU1"
            "&query=any,contains,test%20query&tab=DefaultSlotOrder"
            "&search_scope=MyInstitution&offset=0"
        )
        self.assertEqual(build_helka_url(search_variable), expected_url)

    def test_parse_results(self):
        html = """
        <div class="list-item-wrapper">
            <h3>Test Title / Test Author</h3>
            <a ng-href="https://example.com"></a>
            <div></div><div><span ng-if="::(!$ctrl.isEmailMode())">2024</span></div>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        results = parse_results(soup)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Test Title ")
        self.assertEqual(results[0]["authors"], "Test Author")
        self.assertEqual(results[0]["year"], "2024")
        self.assertEqual(results[0]["doi_link"], "https://example.com")

    def test_extract_result_data(self):
        html = """
        <div class="list-item-wrapper">
            <h3>Test Title / Test Author</h3>
            <a ng-href="https://example.com"></a>
            <div></div><div><span ng-if="::(!$ctrl.isEmailMode())">2024</span></div>
        </div>
        """
        item = BeautifulSoup(html, "html.parser")
        result = extract_result_data(item, 0)

        self.assertEqual(result["result_id"], 0)
        self.assertEqual(result["title"], "Test Title ")
        self.assertEqual(result["authors"], "Test Author")
        self.assertEqual(result["year"], "2024")
        self.assertEqual(result["doi_link"], "https://example.com")

    def test_extract_year(self):
        html = """
        <h3>Test Title</h3>
        <div></div>
        <div>
            <span ng-if="::(!$ctrl.isEmailMode())">2024</span>
        </div>
        """
        h3_element = BeautifulSoup(html, "html.parser").find("h3")
        self.assertEqual(extract_year(h3_element), "2024")

        html = "<h3>Test Title</h3>"
        h3_element = BeautifulSoup(html, "html.parser").find("h3")
        self.assertEqual(extract_year(h3_element), "-")
