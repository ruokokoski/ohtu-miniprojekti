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
    references_dict = [reference.to_dict() for reference in references]
    return references_dict

def list_references_as_bibtex():
    references = Reference.query.order_by(Reference.citation_key).all()
    bib_data = BibliographyData()

    for reference in references:
        bib_entry = Entry(
            reference.entry_type,
            fields={
                'author': reference.author,
                'title': reference.title,
                'year': str(reference.year),
            }
        )

        if reference.extra_fields:
            for key, value in reference.extra_fields.items():
                bib_entry.fields[key] = str(value)

        bib_data.entries[reference.citation_key] = bib_entry

    bibtex_str = bib_data.to_string('bibtex')

    return bibtex_str


'''
def get_bibtex():
    sql = text('SELECT bibtex FROM refs;')
    result = db.session.execute(sql).fetchall()
    return result
'''
