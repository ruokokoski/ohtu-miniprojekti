from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String, JSON
from exceptions import UserInputError
from config import db


class Reference(db.Model):
    __tablename__ = 'refs'

    id = Column(Integer, primary_key=True)
    entry_type = Column(String(50))
    citation_key = Column(String(100), unique=True)
    author = Column(String(255))
    title = Column(String(255))
    year = Column(Integer)
    extra_fields = Column(JSON)  # Tallennetaan JSON-tyyppisenä

    # Kenttäprofiilit eri entry_tyypeille
    FIELD_PROFILES = {
        "article": [
            "month", "journal", "volume", "number", "pages", "note", "doi"
        ],
        "book": [
            "publisher", "address", "volume", "series", "edition",
            "month", "note", "url", "isbn"
        ],
        "booklet": [
            "month", "address", "note", "howpublished", "editor"
        ],
        "conference": [
            "month", "booktitle", "publisher", "address", "pages",
            "note", "editor", "organization"
        ],
        "inbook": [
            "editor", "volume", "number", "series", "address",
            "edition", "month", "pages", "note"
        ],
        "incollection": [
            "booktitle", "publisher", "editor", "volume", "number",
            "series", "pages", "address", "month"
        ],
        "inproceedings": [
            "booktitle","editor", "volume", "number", "series", "pages",
            "address", "month", "organization", "publisher"
        ],
        "manual": [
            "organization", "address", "edition", "month", "note"
        ],
        "mastersthesis": [
            "school", "type", "address", "month", "note"
        ],
        "phdthesis": [
            "school", "type", "address", "month", "note"
        ],
        "proceedings": [
            "editor", "volume", "number", "series", "address", "month", 
            "publisher"
        ],
        "techreport": [
            "institution", "number"
        ],
        "unpublished": [
            "institution"
        ],
        "misc": [
            "howpublished", "note"
        ]
    }

    def get_fields_for_entry_type(self):
        """Palauta extrakenttien nimet tämän entry_type:n perusteella"""
        return self.FIELD_PROFILES.get(self.entry_type, [])
    def get_all_field_profiles(self):
        """palauttaa sanakirjana kaikki viittaustyypit"""
        return self.FIELD_PROFILES

    def to_dict(self):
        data = {
            "entry_type": self.entry_type,
            "citation_key": self.citation_key,
            "author": self.author,
            "title": self.title,
            "year": self.year,
        }
        # Palautetaan extra_fields tai tyhjä sanakirja, jos se on None
        data["extra_fields"] = self.extra_fields if self.extra_fields else {}
        return data

    def save(self):
        """Tallenna viite tietokantaan ja tarkista virheet"""
        try:
            # Haetaan mahdollinen olemassa oleva viite
            existing_reference = db.session.query(Reference).filter_by(
                citation_key=self.citation_key
            ).first()

            # Jos viite löytyy, nostetaan virhe
            if existing_reference:
                error_message = (
                    f"A reference with the citation key '{self.citation_key}' already exists."
                )
                raise UserInputError(error_message)

            db.session.add(self)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            error_message = "An error occurred while saving the reference. Please try again."
            raise UserInputError(error_message) from e

    def update(self, data):
        """Päivitä viite tiedot"""
        try:
            self.entry_type = data["entry_type"]
            self.author = data["author"]
            self.title = data["title"]
            self.year = int(data["year"]) if data["year"] else None
            self.extra_fields = data.get("extra_fields", {})

            db.session.commit()
            print("Update successful!")
        except SQLAlchemyError as e:
            print(f"SQLAlchemy error: {e}")
            db.session.rollback()
