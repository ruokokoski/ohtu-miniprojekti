import unittest
from unittest import mock
from unittest.mock import patch, Mock
from sqlalchemy import text
from entities.reference import Reference
from util import validate_reference, process_reference_form, create_reference, generate_key
from exceptions import UserInputError
from config import create_app, db
from app import app


class TestProcessReferenceForm(unittest.TestCase):
    @patch('util.create_reference')
    @patch('util.validate_reference')
    @patch('util.flash')
    @patch('util.redirect')
    def test_process_reference_form_creation_failure(self, mock_redirect, mock_flash, mock_validate_reference, mock_create_reference):
        mock_validate_reference.side_effect = UserInputError("Invalid input")

        mock_response = mock.Mock()
        mock_response.status_code = 302
        mock_response.location = '/new_reference'
        mock_redirect.return_value = mock_response

        with app.test_request_context('/new_reference', method='POST', data={
            'entry_type': 'book',
            'author': 'Test Author',
            'title': 'Test Title',
            'year': '2024',
            'publisher': 'Test Publisher',
            'address': 'Test Address'
        }):
            result = process_reference_form(is_creation=True)

            self.assertEqual(result.status_code, 302)
            self.assertEqual(mock_response.location, '/new_reference')



class TestReferenceValidation(unittest.TestCase):
    valid_data = {
        "entry_type": "book",
        "key": "Valid123",
        "author": "Valid author",
        "title": "Valid title",
        "year": "2024",
        "extra_fields": {
        "publisher": "Valid Publisher"
    }
    }

    def test_valid_reference_does_not_raise_error(self):
        validate_reference(self.valid_data)

    def test_invalid_year_raises_error(self):
        data = self.valid_data.copy()

        data["year"] = "abcd"

        with self.assertRaises(UserInputError):
            validate_reference(data)


class TestGenerateKey(unittest.TestCase):
    def test_generate_key_valid_input(self):
            author = "Testaaja, Tiina"
            year = "2024"
            title = "Testi otsikko"
            expected_key = "Testaaja2024Testi"
            self.assertEqual(generate_key(author, year, title), expected_key)

    def test_generate_key_non_alphanumeric_title(self):
        author = "Testaaja, Tiina"
        year = "2024"
        title = "Testi!@# otsikko"
        expected_key = "Testaaja2024Testi"
        self.assertEqual(generate_key(author, year, title), expected_key)


class TestUserInputError(unittest.TestCase):
    def test_short_title(self):
        data = {"author": "asd", "title": "A", "year": "2023", "publisher": "Publisher"}
        with self.assertRaises(UserInputError) as context:
            validate_reference(data)
        self.assertEqual(str(context.exception), "Title must be at least 2 characters long.")

    def test_invalid_year(self):
        data = {"author": "asd", "title": "Title", "year": "abcd", "publisher": "Publisher"}
        with self.assertRaises(UserInputError) as context:
            validate_reference(data)
        self.assertEqual(str(context.exception), "Year must be a valid 4-digit number between 1000 and 9999.")

    def test_title_exceeds_max_length(self):
        data = {
            "author": "asd",
            "title": "A" * 251,
            "year": "2024",
            "publisher": "Publisher"
        }
        with self.assertRaises(UserInputError) as context:
            validate_reference(data)
        self.assertEqual(str(context.exception), "Title must be under 250 characters long.")


class TestReferenceModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Testisovelluksen ja testikannan alustaminen"""
        cls.app = create_app()
        cls.client = cls.app.test_client()

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

    def test_to_dict(self):
        """Testaa to_dict-metodia"""
        reference = Reference(
            entry_type='book',
            citation_key='Smith2024My',
            author='Smith, John',
            title='My Book',
            year=2024,
            extra_fields={"publisher": "ABC Press"}
        )
        reference_dict = reference.to_dict()

        self.assertEqual(reference_dict["entry_type"], 'book')
        self.assertEqual(reference_dict["citation_key"], 'Smith2024My')
        self.assertEqual(reference_dict["author"], 'Smith, John')
        self.assertEqual(reference_dict["title"], 'My Book')
        self.assertEqual(reference_dict["year"], 2024)
        self.assertEqual(reference_dict["extra_fields"], {"publisher": "ABC Press"})

    def test_save(self):
        """Testaa save-metodia"""
        reference = Reference(
            entry_type='Article',
            citation_key='Doe2024An',
            author='Doe, Jane',
            title='An Interesting Paper',
            year=2024,
            extra_fields={"journal": "Science"}
        )

        with self.app.app_context():
            reference.save()

        with self.app.app_context():
            saved_reference = Reference.query.filter_by(citation_key='Doe2024An').first()

        self.assertIsNotNone(saved_reference)
        self.assertEqual(saved_reference.citation_key, 'Doe2024An')
        self.assertEqual(saved_reference.author, 'Doe, Jane')
        self.assertEqual(saved_reference.title, 'An Interesting Paper')
        self.assertEqual(saved_reference.year, 2024)
        self.assertEqual(saved_reference.extra_fields, {"journal": "Science"})


    def test_update_success(self):
        """Testaa, että update-metodi päivittää viitteen tiedot oikein"""
        # Luodaan uusi viite
        reference = Reference(
            entry_type='book',
            citation_key='Smith2024My',
            author='Smith, John',
            title='My Book',
            year=2024,
            extra_fields={"publisher": "ABC Press"}
        )

        with app.app_context():
            db.session.add(reference)
            db.session.commit()

        updated_data = {
            "entry_type": "book",
            "author": "Doe, Jane",
            "title": "Updated Paper",
            "year": 2025,
            "extra_fields": {"publisher": "ABC Press"}
        }

        with app.app_context():
            reference_to_update = Reference.query.filter_by(citation_key='Smith2024My').first()

            if reference_to_update:
                reference_to_update.update(updated_data)
                db.session.commit()

        with app.app_context():
            reference.update(updated_data)
            db.session.commit()

        with app.app_context():
            updated_reference = Reference.query.filter_by(citation_key='Smith2024My').first()

        self.assertEqual(updated_reference.entry_type, "book")
        self.assertEqual(updated_reference.author, "Doe, Jane")
        self.assertEqual(updated_reference.title, "Updated Paper")
        self.assertEqual(updated_reference.year, 2025)
        self.assertEqual(updated_reference.extra_fields, {"publisher": "ABC Press"})

class ReferenceModelTestInproceedings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Testauksen valmistelu, luodaan Flask-sovellus ja tietokanta"""
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Testauksen jälkeinen siivous, poistetaan tietokanta"""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_inproceedings_reference(self):
        """Testaa, että inproceedings-tyyppinen viite voidaan tallentaa tietokantaan"""
        data = {
            "entry_type": "inproceedings",
            "author": "John Doe",
            "title": "Research Paper Title",
            "year": "2023",
            "extra_fields": {
                "booktitle": "Conference Proceedings",
                "publisher": "Publisher Name",
                "address": "Conference City"
            }
        }

        # Luo viite
        reference = Reference(
            entry_type=data["entry_type"],
            citation_key="Doe2023Research",  # Käytetään oletettua arvoa, varmista että se on uniikki
            author=data["author"],
            title=data["title"],
            year=data["year"],
            extra_fields=data["extra_fields"]
        )

        # Tallenna viite
        reference.save()

        # Tarkista, että viite on tallennettu tietokantaan
        saved_reference = Reference.query.filter_by(citation_key="Doe2023Research").first()
        self.assertIsNotNone(saved_reference)
        self.assertEqual(saved_reference.entry_type, "inproceedings")
        self.assertEqual(saved_reference.author, "John Doe")
        self.assertEqual(saved_reference.title, "Research Paper Title")
        self.assertEqual(saved_reference.year, 2023)
        self.assertEqual(saved_reference.extra_fields["booktitle"], "Conference Proceedings")

if __name__ == "__main__":
    unittest.main()
