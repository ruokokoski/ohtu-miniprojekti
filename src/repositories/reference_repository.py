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

def delete_reference(citation_key):
    sql = text('DELETE FROM books WHERE "key" = :key')
    db.session.execute(sql, {"key": citation_key})
    db.session.commit()

def create_entry_from_row(row):
    # Luo ja palauttaa Pybtex Entry-objektin rivin tiedoista
    author = str(row.author) if row.author else ''
    title = str(row.title) if row.title else ''
    year = str(row.year) if row.year is not None else ''
    publisher = str(row.publisher) if row.publisher else ''
    address = str(row.address) if row.address else ''
    volume = str(row.volume) if row.volume else ''
    series = str(row.series) if row.series else ''
    edition = str(row.edition) if row.edition else ''
    month = str(row.month) if row.month else ''
    note = str(row.note) if row.note else ''
    url = str(row.url) if row.url else ''

    # Luo Pybtex Entry-objekti
    entry = Entry('book', {
        'author': author,
        'title': title,
        'year': year,
        'publisher': publisher,
        'address': address,
        'volume': volume,
        'series': series,
        'edition': edition,
        'month': month,
        'note': note,
        'url': url
    })
    return entry

def list_references_as_bibtex():
    # Suoritetaan SQL-kysely ja haetaan kaikki viitteet
    sql = text('SELECT author, year, title, publisher, address, key '
        ' FROM books '
        'ORDER BY key')
    result = db.session.execute(sql).fetchall()

    # Luo BibliographyData-objekti, johon viitteet lisätään
    bib_data = BibliographyData()

    for row in result:
        if not row:
            continue

        entry = create_entry_from_row(row)

        # Lisää viite BibTeX-tietokantaan käyttäen viitteen avainta ('key')
        bib_data.add_entry(row.key, entry)

    # Palautetaan BibTeX-tiedot Pybtexin `to_string()`-metodilla
    return bib_data.to_string('bibtex')


def get_bibtex():
    sql = text('SELECT bibtex FROM refs;')
    result = db.session.execute(sql).fetchall()
    return result
