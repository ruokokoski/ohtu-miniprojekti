import unittest
from unittest.mock import MagicMock, patch
from repositories.reference_repository import list_references_as_bibtex
from pybtex.database import Entry


class TestListReferencesAsBibtex(unittest.TestCase):

    @patch('config.db.session.execute')
    def test_sql_query_execution(self, mock_execute):
        mock_execute.return_value.fetchall.return_value = [
            MagicMock(key='key1', author='Author1', year=2024, title='Title1',
                      publisher='Publisher1', address='Address1', volume='',
                      series='', edition='', month='', note='', url=''),
            MagicMock(key='key2', author='Author2', year=2023, title='Title2',
                      publisher='Publisher2', address='Address2', volume='',
                      series='', edition='', month='', note='', url='')
        ]

        result = list_references_as_bibtex()

        print(f"Mocked data: {mock_execute.return_value.fetchall.return_value}")
        print(f"Result length (BibTeX entries): {result.count('@book')}")

        # Tarkistetaan, että SQL-kysely suoritettiin
        mock_execute.assert_called_once()
        self.assertEqual(result.count('@book'), 2)  # Odotetaan kahta viitettä

    @patch('config.db.session.execute')
    def test_reference_processing(self, mock_execute):
        mock_execute.return_value.fetchall.return_value = [
            MagicMock(key='key1', author='Author1', year=2024, title='Title1',
                      publisher='Publisher1', address='', volume='', series='',
                      edition='', month='', note='', url='')
        ]
        
        result = list_references_as_bibtex()

        # Tarkistetaan, että viitteen kenttä 'address' on tyhjä, koska sitä ei ole tietokannassa
        self.assertIn('author = "Author1"', result)
        self.assertIn('year = "2024"', result)
        self.assertIn('address = ""', result)  # Tarkistetaan, että puuttuva kenttä on tyhjä

    @patch('config.db.session.execute')
    def test_year_conversion(self, mock_execute):
        mock_execute.return_value.fetchall.return_value = [
            MagicMock(key='key1', author='Author1', year=2024, title='Title1',
                      publisher='Publisher1', address='', volume='', series='',
                      edition='', month='', note='', url='')
        ]
        
        result = list_references_as_bibtex()

        # Tarkistetaan, että vuosi on muunnettu merkkijonoksi
        self.assertIn('year = "2024"', result)

    @patch('config.db.session.execute')
    @patch('pybtex.database.BibliographyData.add_entry')
    def test_bibtex_entry_creation(self, mock_add_entry, mock_execute):
        mock_execute.return_value.fetchall.return_value = [
            MagicMock(key='key1', author='Author1', year=2024, title='Title1',
                      publisher='Publisher1', address='', volume='', series='',
                      edition='', month='', note='', url='')
        ]
        
        list_references_as_bibtex()
        
        # Varmistetaan, että add_entry-metodia kutsutaan kerran
        mock_add_entry.assert_called_once()
        
        # Tarkistetaan, että oikea key ja Entry-objekti on annettu
        args, _ = mock_add_entry.call_args
        self.assertEqual(args[0], 'key1')  # Tarkistetaan, että oikea key käytettiin
        self.assertTrue(isinstance(args[1], Entry))  # Tarkistetaan, että lisätty objekti on Entry

    @patch('config.db.session.execute')
    def test_missing_fields(self, mock_execute):
        mock_execute.return_value.fetchall.return_value = [
            MagicMock(key='key1', author='Author1', year=2024, title='Title1',
                      publisher='Publisher1', address='', volume='', series='',
                      edition='', month='', note='', url='')
        ]
        
        result = list_references_as_bibtex()

        # Varmistetaan, että puuttuvat kentät ovat tyhjiä
        self.assertIn('series = ""', result)
        self.assertIn('note = ""', result)

    @patch('config.db.session.execute')
    def test_bibtex_format(self, mock_execute):
        mock_execute.return_value.fetchall.return_value = [
            MagicMock(key='key1', author='Author1', year=2024, title='Title1',
                      publisher='Publisher1', address='', volume='', series='',
                      edition='', month='', note='', url='')
        ]
        
        result = list_references_as_bibtex()

        # Tarkistetaan, että palautettu muoto on BibTeX-yhteensopiva
        self.assertTrue(result.startswith('@book{key1,'))
        self.assertTrue('author = "Author1"' in result)
        self.assertTrue('year = "2024"' in result)