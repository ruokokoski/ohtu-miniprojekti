import unittest
from unittest.mock import patch
from sqlalchemy import text
from repositories.reference_repository import list_references

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
        self.assertEqual(str(called_sql_query), str(text('SELECT author, year, title, publisher, address, key '
                                                     ' FROM books '
                                                     'ORDER BY author DESC')))
        self.assertEqual(result, mock_data)
