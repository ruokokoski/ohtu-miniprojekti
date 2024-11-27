from sqlalchemy import text
from pybtex.database import BibliographyData, Entry
from entities.reference import Reference
from config import db



def get_reference_by_key(key):
    sql = text(
        """
        SELECT key, author, year, title, publisher, address, 
               volume, series, edition, month, note, url
        FROM books
        WHERE key = :key
        """
    )
    result = db.session.execute(sql, {"key": key}).fetchone()
    return result

def update_reference(data):
    sql = text(
        """
        UPDATE books
        SET
        key = :key,  author = :author, year = :year,
        title = :title, publisher = :publisher, address = :address,
        volume = :volume, series = :series, edition = :edition,
        month = :month, note = :note, url = :url
        WHERE key = :key
        """
    )
    db.session.execute(sql, data)
    db.session.commit()

def delete_reference(key):
    sql = text("DELETE FROM books WHERE key = :key")
    db.session.execute(sql, {"key": key})
    db.session.commit()


def list_references_as_bibtex():
    # Haetaan kaikki viitteet tietokannasta
    references = Reference.query.all()
    bib_data = BibliographyData()

    # Käydään läpi kaikki viitteet ja luodaan niistä BibTeX-kenttiä
    for reference in references:
        # Määritellään BibTeX-tiedot
        bib_entry = Entry(
            reference.entry_type,  # Entry type, esim. 'book' tai 'article'
            fields={
                'author': reference.author,
                'title': reference.title,
                'year': str(reference.year),
            }
        )

        # Lisätään mahdolliset extra_fields
        if reference.extra_fields:
            for key, value in reference.extra_fields.items():
                bib_entry.fields[key] = str(value)

        # Lisätään BibTeX-tieto bib_data-objektiin käyttäen citation key:tä
        bib_data.entries[reference.citation_key] = bib_entry

    # Muunnetaan BibTeX-objekti merkkijonoksi
    bibtex_str = bib_data.to_string('bibtex')

    return bibtex_str


'''
def get_bibtex():
    sql = text('SELECT bibtex FROM refs;')
    result = db.session.execute(sql).fetchall()
    return result
'''
