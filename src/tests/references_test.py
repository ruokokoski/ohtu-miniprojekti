import unittest
from unittest import mock
from unittest.mock import patch, Mock
from sqlalchemy import text
from repositories.reference_repository import list_references_as_dict, delete_reference
from entities.reference import Reference
from util import validate_reference, process_reference_form, create_reference, generate_key
from exceptions import UserInputError
from app import app


class TestProcessReferenceForm(unittest.TestCase):
    @patch('util.create_reference')
    @patch('util.validate_reference')
    @patch('util.flash')
    @patch('util.redirect')
    def test_process_reference_form_creation_failure(self, mock_redirect, mock_flash, mock_validate_reference, mock_create_reference):
        # Simulate validation failure
        mock_validate_reference.side_effect = UserInputError("Invalid input")

        # Create a mock response object
        mock_response = mock.Mock()
        mock_response.status_code = 302
        mock_response.location = '/new_reference'  # Set the location explicitly
        mock_redirect.return_value = mock_response

        # Simulate the test request context
        with app.test_request_context('/new_reference', method='POST', data={
            'entry_type': 'book',
            'author': 'Test Author',
            'title': 'Test Title',
            'year': '2024',
            'publisher': 'Test Publisher',
            'address': 'Test Address'
        }):
            # Call the function under test
            result = process_reference_form(is_creation=True)

            # Assertions
            self.assertEqual(result.status_code, 302)  # Check that the status code is 302 (Redirect)
            self.assertEqual(mock_response.location, '/new_reference')  # Check that the location is '/new_reference'



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
            "title": "A" * 101,
            "year": "2024",
            "publisher": "Publisher"
        }
        with self.assertRaises(UserInputError) as context:
            validate_reference(data)
        self.assertEqual(str(context.exception), "Title must be under 100 characters long.")
