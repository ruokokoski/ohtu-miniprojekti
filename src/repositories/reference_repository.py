from sqlalchemy.exc import SQLAlchemyError
from pybtex.database import BibliographyData, Entry, parse_string
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

def bibtex_to_dict(bibtex_str):
    bib_data = parse_string(bibtex_str, "bibtex")

    result = {}

    for entry in bib_data.entries.values():
        fields = {}

        for field, value in entry.fields.items():
            fields[field] = value

        fields['entry_type'] = entry.type

        if 'author' in entry.persons:
            authors = entry.persons['author']
            author_names = [str(person) for person in authors]
            fields['author'] = " and ".join(author_names)

        result = fields
    return result
