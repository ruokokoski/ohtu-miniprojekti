from sqlalchemy import text
from pybtex.database import BibliographyData, Entry
from config import db

def list_references():
    sql = text('SELECT author, year, title, publisher, address, key '
        ' FROM books '
        'ORDER BY key')
    result = db.session.execute(sql).fetchall()
    return result

def create_reference(data):

    columns = ', '.join(data.keys()) # (col1, col2...)
    placeholders = ', '.join(f":{key}" for key in data.keys()) # (:col1, :col2...)

    sql_query = text(f"""INSERT INTO Books ({columns}) VALUES ({placeholders})""")

    db.session.execute(sql_query, data)
    db.session.commit()

def delete_reference(key):
    sql = text("DELETE FROM books WHERE key = :key")
    db.session.execute(sql, {"key": key})
    db.session.commit()

def list_references_as_bibtex():
    # Suoritetaan SQL-kysely ja haetaan kaikki viitteet
    sql = text('SELECT author, year, title, publisher, address, key '
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


        # Luo Pybtex Entry-objekti jokaiselle kirjalle
        entry = Entry('book', {
            'author': author,
            'title': title,
            'year': year,
            'publisher': publisher,
            'address': address
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
