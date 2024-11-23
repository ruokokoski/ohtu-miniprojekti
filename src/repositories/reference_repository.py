from sqlalchemy import text
from pybtex.database import BibliographyData, Entry
from config import db

def list_references():
    sql = text(
        """
        SELECT key, author, year, title, publisher, address, 
               volume, series, edition, month, note, url
        FROM books
        ORDER BY key
        """
    )
    result = db.session.execute(sql).fetchall()
    return result


def create_reference(data):
    sql_query = text(
        """
        INSERT INTO books (
            key, author, year, title, publisher, address,
            volume, series, edition, month, note, url
        )
        VALUES (
            :key, :author, :year, :title, :publisher, :address,
            :volume, :series, :edition, :month, :note, :url
        )
        """
    )
    db.session.execute(sql_query, data)
    db.session.commit()


def delete_reference(key):
    sql = text("DELETE FROM books WHERE key = :key")
    db.session.execute(sql, {"key": key})
    db.session.commit()


def list_references_as_bibtex():
    sql = text("""
        SELECT key, author, year, title, publisher, address,
               volume, series, edition, month, note, url
        FROM books
        ORDER BY key
    """)
    result = db.session.execute(sql).fetchall()

    # Luo BibliographyData-objekti BibTeX-tietojen tallentamiseen
    bib_data = BibliographyData()

    # Käydään läpi kaikki viitteet ja lisätään ne BibTeX-tietokantaan
    for row in result:
        entry_data = {field: getattr(row, field, '') or '' for field in [
            'author', 'title', 'year', 'publisher', 'address', 'volume',
            'series', 'edition', 'month', 'note', 'url']}

        # Muunna vuosi merkkijonoksi
        entry_data['year'] = str(entry_data['year'])

        # Luo ja lisää viite BibTeX-tietokantaan
        bib_data.add_entry(row.key, Entry('book', entry_data))

    # Palautetaan BibTeX-tiedot Pybtexin `to_string()`-metodilla
    return bib_data.to_string('bibtex')


def get_bibtex():
    sql = text('SELECT bibtex FROM refs;')
    result = db.session.execute(sql).fetchall()
    return result
