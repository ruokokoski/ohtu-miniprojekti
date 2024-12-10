import unittest
from io import BytesIO
from unittest.mock import patch
from app import app
from entities.reference import Reference
from sqlalchemy.exc import SQLAlchemyError
from flask import flash, redirect

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()


    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"BibTeX-reference manager", response.data)


    def test_new_reference_route(self):
        response = self.client.get("/new_reference")
        self.assertEqual(response.status_code, 200)
        #self.assertIn(b"New Reference", response.data)


    @patch("app.process_reference_form")
    def test_create_reference_route(self, mock_process_reference_form):
        mock_process_reference_form.return_value = redirect("/references")
        response = self.client.post("/create_reference", data={
            "citation_key": "TestKey",
            "author": "Author Test",
            "title": "Test Title"
        })
        mock_process_reference_form.assert_called_once_with(is_creation=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/references")


    @patch("app.list_references_as_dict")
    def test_browse_references_route(self, mock_list_references_as_dict):
        mock_list_references_as_dict.return_value = [
            {
                "citation_key": "TestKey",
                "title": "Test Title",
                "extra_fields": {"field1": "value1", "field2": "value2"}
            }
        ]
        response = self.client.get("/references")
        mock_list_references_as_dict.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Title", response.data)

    @patch("app.get_reference_by_key")
    def test_edit_reference_route(self, mock_get_reference_by_key):
        mock_get_reference_by_key.return_value = Reference(
            citation_key="Author2020Test",
            entry_type="journal",
            author="Author, John",
            title="Test Title",
            year="2020",
            extra_fields={"journal": "Test Journal"}
        )
        response = self.client.get("/edit_reference/Author2020Test")
        mock_get_reference_by_key.assert_called_once_with("Author2020Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Title", response.data)


    @patch("app.process_reference_form")
    def test_update_reference_route(self, mock_process_reference_form):
        mock_process_reference_form.return_value = redirect("/references")
        response = self.client.post("/update_reference", data={
            "citation_key": "TestKey",
            "entry_type": "book",
            "author": "Updated Author",
            "title": "Updated Title",
            "year":"2020",
            "extra_fields":{"publisher": "Test Publisher"}
        })
        mock_process_reference_form.assert_called_once_with(is_creation=False, citation_key="TestKey")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/references")


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


    @patch("app.process_reference_form")
    def test_from_search_new_reference_post(self, mock_process_reference_form):
        mock_process_reference_form.return_value = {"message": "Reference added successfully"}
        response = self.client.post("/popup_new_search_reference/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Reference added successfully", response.data)


    @patch("app.list_references_as_bibtex")
    def test_download_file(self, mock_list_references_as_bibtex):
        mock_list_references_as_bibtex.return_value = "mocked bibtex data"
        response = self.client.get("/download")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Disposition'], 'attachment; filename=references.bib')
        self.assertEqual(response.data, b"mocked bibtex data")


    def test_download_references(self):
        response = self.client.post("/download")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['message'], "Your BibTeX references file is ready for download.")
        self.assertEqual(json_data['status'], "success")

    @patch("app.reset_db")
    def test_reset_database(self, mock_reset_db):
        response = self.client.get("/reset_db")
        self.assertEqual(response.status_code, 200)
        mock_reset_db.assert_called_once()
        json_data = response.get_json()
        self.assertEqual(json_data['message'], "db reset")
