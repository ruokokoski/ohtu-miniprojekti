from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.exc import SQLAlchemyError
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
        """Tallenna viite tietokantaan"""
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Päivitä viite tiedot"""
        try:
            self.entry_type = data["entry_type"]
            self.author = data["author"]
            self.title = data["title"]
            self.year = int(data["year"]) if data["year"] else None
            self.extra_fields = data.get("extra_fields", {})

            db.session.commit()
            print("Päivitys onnistui!")
        except SQLAlchemyError as e:
            print(f"SQLAlchemy virhe päivityksessä: {e}")
            db.session.rollback()
