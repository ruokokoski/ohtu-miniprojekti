from sqlalchemy import text
from pybtex.database import BibliographyData, Entry
from config import db

def list_references():
    sql = text('SELECT author, year, title, publisher, address, volume, series, '
        'edition, month, note, url, key '
        ' FROM books '
        'ORDER BY key')
    result = db.session.execute(sql).fetchall()
    return result

def create_reference(data):

    sql_query = text("""INSERT INTO books (author, year, title, publisher, address, key)
                    VALUES (:author, :year, :title, :publisher, :address, :key)""")

    db.session.execute(sql_query, data)
    db.session.commit()

def delete_reference(key):
    sql = text("DELETE FROM books WHERE key = :key")
    db.session.execute(sql, {"key": key})
    db.session.commit()

def list_references_as_bibtex():
    # Suoritetaan SQL-kysely ja haetaan kaikki viitteet
    sql = text('SELECT author, year, title, publisher, address, volume, series, '
        'edition, month, note, url, key '
        ' FROM books '
        'ORDER BY key')
    result = db.session.execute(sql).fetchall()

    # Luo BibliographyData-objekti, johon viitteet lisätään
    bib_data = BibliographyData()

    for row in result:
        # Jos tulos on None, ohitetaan
        if not row:
            continue

        # Muutetaan kaikki kentät merkkijonoiksi varmistaaksemme, että Pybtex ei kohtaa virheitä
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

        # Luo Pybtex Entry-objekti kirjalle, mukaan lukien uudet kentät
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

        # Lisää viite BibTeX-tietokantaan käyttäen viitteen avainta ('key')
        bib_data.add_entry(row.key, entry)

    # Palautetaan BibTeX-tiedot Pybtexin `to_string()`-metodilla
    return bib_data.to_string('bibtex')


#resultista voi muodostaa APA-listauksen:
def get_bibtex():
    sql = text('SELECT bibtex FROM refs;')
    result = db.session.execute(sql).fetchall()
    return result
