from sqlalchemy.exc import SQLAlchemyError
from pybtex.database import BibliographyData, Entry
from entities.reference import Reference
from config import db


def get_reference_by_key(key):
    """Palauta viite citation_key:n perusteella"""
    reference = Reference.query.filter_by(citation_key=key).first()
    return reference

def delete_reference(key):
    """Poista viite Key:n perusteella"""
    reference = get_reference_by_key(key)
    if reference:
        try:
            db.session.delete(reference)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"Database error: {str(e)}") from e
    else:
        raise ValueError(f"Reference {key} not found.")

def list_references_as_dict():
    references = Reference.query.order_by(Reference.citation_key).all()
    # Muutetaan jokainen Reference-olio sanakirjaksi
    references_dict = [reference.to_dict() for reference in references]
    return references_dict

def list_references_as_bibtex():
    # Haetaan kaikki viitteet tietokannasta
    references = Reference.query.order_by(Reference.citation_key).all()
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
