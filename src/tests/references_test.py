import unittest
from unittest.mock import patch
from sqlalchemy import text
from repositories.reference_repository import list_references, create_reference
from util import validate_reference, UserInputError
from app import app

class TestReferences(unittest.TestCase):
    @patch('repositories.reference_repository.db.session.execute')
    def test_list_references(self, mock_execute):
        mock_data = [
            ("Christopher Bishop", 2024, "Deep Learning", "Springer", "UK", "bishop2024"),
            ("Kevin Murphy", 2022, "Probabilistic Machine learning", "MIT", "-", "murphy2022"),
        ]
        mock_execute.return_value.fetchall.return_value = mock_data

        result = list_references()
        called_sql_query = mock_execute.call_args[0][0]
        self.assertEqual(str(called_sql_query), str(text('SELECT author, year, title, publisher, '
                                                         'address, volume, series, '
                                                        'edition, month, note, url, key '
                                                     ' FROM books '
                                                     'ORDER BY key')))
        self.assertEqual(result, mock_data)

    @patch("repositories.reference_repository.db.session.execute")
    def test_create_reference(self, mock_execute):
        mock_data = {
            "key": "mock key",
            "author": "mock author",
            "title": "mock title",
            "publisher": "mock publisher",
            "address": "mock address",
            "year": "2023"
        }

        expected_sql_query = str(text("""INSERT INTO books (author, year, title, publisher, address, volume, series,
                                        edition, month, note, url, key)
                    VALUES (:author, :year, :title, :publisher, :address, :volume, :series,
                            :edition, :month, :note, :url, :key)"""))

        with app.app_context():
            create_reference(mock_data)
            called_sql_query = mock_execute.call_args[0][0]
            print(expected_sql_query)
            print(called_sql_query)
            self.assertEqual(str(called_sql_query), expected_sql_query)

class TestReferenceValidation(unittest.TestCase):
    valid_data = {
        "key": "Valid123",
        "author": "Valid author",
        "title": "Valid title",
        "publisher": "Valid publisher",
        "address": "Valid address",
        "year": "2023"
    }

    def test_valid_reference_does_not_raise_error(self):
        validate_reference(self.valid_data)

#    def test_too_short_or_long_raises_error(self):
#        short_data = self.valid_data.copy()
#        long_data = self.valid_data.copy()

#        short_data["author"] = ""
#        long_data["author"] = "abc" * 100

#        with self.assertRaises(UserInputError):
#            validate_reference(short_data)

#        with self.assertRaises(UserInputError):
#            validate_reference(long_data)


    def test_invalid_year_raises_error(self):
        data = self.valid_data.copy()

        data["year"] = "abcd"

        with self.assertRaises(UserInputError):
            validate_reference(data)
