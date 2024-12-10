import unittest
from entities.reference import Reference
from repositories.reference_repository import (
    list_references_as_dict,
    delete_reference,
    get_reference_by_key,
    list_references_as_bibtex,
    bibtex_to_dict
)
from collections import OrderedDict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from config import create_app, db
from app import app


class TestReferenceModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Testisovelluksen ja testikannan alustaminen"""
        cls.app = create_app()
        cls.client = cls.app.test_client()
    
        # Varmista, että tietokanta on tyhjä ennen testejä
        with cls.app.app_context():
            cls.client.get('/reset_db')
            db.create_all()

    def setUp(self):
        """Suoritetaan ennen jokaista testiä"""
        with app.app_context():
            self.reference = Reference(
                entry_type="book",
                citation_key="Test2024",
                author="John Smith",
                title="My Test Book",
                year=2024,
                extra_fields={"publisher": "Test Publisher"}
            )
            db.session.add(self.reference)
            db.session.commit()

    def tearDown(self):
        """Poistaa vain tiedot tauluista testin jälkeen"""
        with self.app.app_context():
            db.session.execute(text("TRUNCATE TABLE refs RESTART IDENTITY CASCADE"))
            db.session.commit()

    def test_get_reference_by_key(self):
        """Testaa, että viite haetaan citation_key:n perusteella"""
        with app.app_context():
            ref = get_reference_by_key("Test2024")
            self.assertIsNotNone(ref)
            self.assertEqual(ref.citation_key, "Test2024")
            self.assertEqual(ref.author, "John Smith")

    def test_get_reference_by_invalid_key(self):
        """Testaa, että virheellinen key palauttaa None"""
        with app.app_context():
            ref = get_reference_by_key("InvalidKey")
            self.assertIsNone(ref)

    def test_delete_reference(self):
        """Testaa, että viite poistetaan key:n perusteella"""
        with app.app_context():
            delete_reference("Test2024")
            ref = get_reference_by_key("Test2024")
            self.assertIsNone(ref)

    def test_delete_reference_invalid_key(self):
        """Testaa, että virheellinen key nostaa virheen"""
        with app.app_context():
            with self.assertRaises(ValueError):
                delete_reference("InvalidKey")

    def test_list_references_as_dict(self):
        """Testaa, että kaikki viitteet listataan sanakirjana"""
        with app.app_context():
            ref_list = list_references_as_dict()
            self.assertEqual(len(ref_list), 1)
            self.assertEqual(ref_list[0]["citation_key"], "Test2024")

    def test_list_references_as_bibtex(self):
        """Testaa, että viitteet listataan BibTeX-muodossa"""
        with app.app_context():
            bibtex_str = list_references_as_bibtex()
            self.assertIn("@book", bibtex_str)  # Tarkistetaan, että BibTeX-formaatti sisältää @book
            self.assertIn("Test2024", bibtex_str)  # Tarkistetaan, että viitteen citation_key löytyy


class TestBibtexToDict(unittest.TestCase):
    def test_single_entry(self):
        """Testaa yhden BibTeX-tietueen muuntamista sanakirjaksi."""
        bibtex_str = """
        @article{sample2024,
          author = {Doe, John},
          title = {Sample Paper},
          journal = {Sample Journal},
          year = {2024},
          volume = {10},
          pages = {100-110},
        }
        """
        expected_output = {
                'entry_type': 'article',
                'author': 'Doe, John',
                'title': 'Sample Paper',
                'journal': 'Sample Journal',
                'year': '2024',
                'volume': '10',
                'pages': '100-110'
        }

        result = bibtex_to_dict(bibtex_str)
        self.assertEqual(sorted(result.items()), sorted(expected_output.items()))

    def test_multible_authors(self):
        """Testaa yhden BibTeX-tietueen muuntamista sanakirjaksi."""
        bibtex_str = """
        @article{sample2024,
          author = {Doe, Tina and Smith, Peter and Baker, Alice},
          title = {Sample Paper},
          journal = {Sample Journal},
          year = {2024},
          volume = {10},
          pages = {100-110},
        }
        """

        expected_output = {
                'entry_type': 'article',
                'author': 'Doe, Tina and Smith, Peter and Baker, Alice',
                'title': 'Sample Paper',
                'journal': 'Sample Journal',
                'year': '2024',
                'volume': '10',
                'pages': '100-110'
        }

        result = bibtex_to_dict(bibtex_str)
        self.assertEqual(sorted(result.items()), sorted(expected_output.items()))
