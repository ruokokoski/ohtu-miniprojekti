import unittest
from unittest.mock import patch
from app import app
from sqlalchemy.exc import SQLAlchemyError
from flask import flash

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_new_reference_route(self):
        response = self.client.get("/new_reference")
        self.assertEqual(response.status_code, 200)

    @patch("app.list_references")
    def test_browse_references_route(self, mock_list_references):
        mock_data = [
            {"author": "Testaaja, Testi", "year": "2024", "title": "Listan testaus"}
        ]
        mock_list_references.return_value = mock_data

        response = self.client.get("/references")

        self.assertEqual(response.status_code, 200)
        mock_list_references.assert_called_once()

    @patch("app.delete_reference")
    @patch("app.flash")
    def test_delete_reference_route_failure(self, mock_flash, mock_delete_reference):
        mock_delete_reference.side_effect = SQLAlchemyError("Tietokantavirhe")

        key = "Testaaja2024Listan"
        response = self.client.post(f"/delete_reference/{key}")
        mock_delete_reference.assert_called_once_with(key)

        mock_delete_reference.assert_called_once_with(key)
        mock_flash.assert_called_once_with("Virhe viitteen poistamisessa: Tietokantavirhe", "failure")

    @patch("app.delete_reference")
    @patch("app.flash")
    def test_delete_reference_route_success(self, mock_flash, mock_delete_reference):
        mock_delete_reference.return_value = None

        key = "Testaaja2024Listan"
        response = self.client.post(f"/delete_reference/{key}")
        mock_delete_reference.assert_called_once_with(key)

        mock_flash.assert_called_once_with("Viite poistettu onnistuneesti", "success")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/references")