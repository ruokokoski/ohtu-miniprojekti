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

    @patch("app.delete_reference")
    @patch("app.flash")
    def test_delete_reference_route_failure(self, mock_flash, mock_delete_reference):
        mock_delete_reference.side_effect = SQLAlchemyError("Tietokantavirhe")

        key = "Testaaja2024Listan"
        response = self.client.post(f"/delete_reference/{key}")
        mock_delete_reference.assert_called_once_with(key)

        mock_delete_reference.assert_called_once_with(key)
        mock_flash.assert_called_once_with("Error when deleting reference: Tietokantavirhe", "failure")

    @patch("app.delete_reference")
    @patch("app.flash")
    def test_delete_reference_route_success(self, mock_flash, mock_delete_reference):
        mock_delete_reference.return_value = None

        key = "Testaaja2024Listan"
        response = self.client.post(f"/delete_reference/{key}")
        mock_delete_reference.assert_called_once_with(key)

        mock_flash.assert_called_once_with("Reference deleted", "success")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/references")