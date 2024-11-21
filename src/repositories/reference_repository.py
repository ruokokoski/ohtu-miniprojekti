from sqlalchemy import text
from pybtex.database import BibliographyData, Entry
from pybtex.database import parse_string
from config import db

def list_references():
    sql = text("SELECT author, year, title, publisher, address, key "
        " FROM books "
        "ORDER BY key")
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


def get_bibtex():
    sql = text("SELECT bibtex FROM refs;")
    result = db.session.execute(sql).fetchall()
    return result

def format_apa_entry(entry):
    citation_key = entry.key if hasattr(entry, 'key') else "Unknown"
    authors = entry.persons.get('author', [])
    author_names = " and ".join(
        [" ".join(person.first() + person.last()) for person in authors]
    ) if authors else "Unknown"
    year = entry.fields.get('year', 'n.d.')
    title = entry.fields.get('title', 'Untitled')
    publisher = entry.fields.get('publisher', 'Unknown')
    #optionaaliset kentät: address, volume, series, edition, month, note, url
    address = entry.fields.get('address', '')
    volume = entry.fields.get('volume', '')
    series = entry.fields.get('series', '')
    edition = entry.fields.get('edition', '')
    month = entry.fields.get('month', '')
    note = entry.fields.get('note', '')
    url = entry.fields.get('url', '')

    apa_entry = f"{author_names} ({year}). {title}."
    if edition:
        apa_entry += f" ({edition} ed.)."
    if volume:
        apa_entry += f" Vol. {volume}."
    if series:
        apa_entry += f" {series}."
    if publisher:
        apa_entry += f" {publisher}{', ' + address if address else ''}."
    if month:
        apa_entry += f" ({month})."
    if note:
        apa_entry += f" {note}."
    if url:
        apa_entry += f" Retrieved from {url}"
    return citation_key, apa_entry

def bibtex_to_apa():
    bibtex_data = get_bibtex()
    apa_bibliography = []
    for entry in bibtex_data:
        bibtex_entry = entry[0]
        try:
            parsed_data = parse_string(bibtex_entry, "bibtex")
            for _, entry_data in parsed_data.entries.items():
                print(f"Parsittu data: {entry_data.fields}")
                formatted_entry = format_apa_entry(entry_data)
                apa_bibliography.append(formatted_entry)
        except KeyError as e:
            print(f"Virhe bibtexin käsittelyssä: {bibtex_entry}\n{e}")
    return apa_bibliography
