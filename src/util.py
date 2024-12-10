import re
from flask import redirect, request, flash
from entities.reference import Reference
from repositories.reference_repository import get_reference_by_key
from exceptions import UserInputError



def process_reference_form(is_creation, citation_key=None):
    """Käsittelee lomakkeen tiedot ja suorittaa validoinnin."""
    # Haetaan formista lähetetyt tiedot
    entry_type = request.form.get('entry_type', '')
    author = request.form.get('author', '')
    title = request.form.get('title', '')
    year = request.form.get('year', '')


    extra_fields = create_extra_fields(entry_type)


    # Luo data-sanakirja
    data = {
        "entry_type": entry_type,
        "author": author,
        "title": title,
        "year": year,
        "extra_fields": extra_fields
    }
    print(data)

    if not is_creation and citation_key:
        data['citation_key'] = citation_key

    # Suoritetaan validointi
    try:
        validate_reference(data)

        # Luo uusi viite tai päivitä olemassa oleva
        if is_creation:
            create_reference(data)
            flash("New reference created", "success")
        else:
            update_reference(citation_key, data)
            flash("Reference updated", "success")

        return redirect("/references")

    except UserInputError as error:
        flash(str(error), "failure")
        redirect_url = (
            "/new_reference" if is_creation
            else f"/edit_reference/{data['citation_key']}"
        )
        return redirect(redirect_url)

def create_extra_fields(entry_type):
    """Palauttaa dynaamiset extra_fields-kentät viitetyypin mukaan"""
    extra_fields = {}

    fields_for_entry = Reference.FIELD_PROFILES.get(entry_type, {})

    required_fields = fields_for_entry.get("required", [])
    optional_fields = fields_for_entry.get("optional", [])

    exclude_fields = ["author", "title", "year"]

    for field in required_fields + optional_fields:
        if field not in exclude_fields:
            extra_fields[field] = request.form.get(field, '')

    return extra_fields


def create_reference(data):
    """Luo uusi viite ja tallenna se tietokantaan"""
    citation_key = generate_key(data['author'], data['year'], data['title'])

    reference = Reference(
        entry_type=data['entry_type'],
        citation_key=citation_key,
        author=data['author'],
        title=data['title'],
        year=data['year'],
        extra_fields=data['extra_fields']
    )
    reference.save()


def update_reference(citation_key, data):
    """Päivitä olemassa oleva viite"""
    reference = get_reference_by_key(citation_key)
    reference.update(data)


def validate_reference(reference):
    """Suorita yleinen validointi"""
    validate_author(reference)
    validate_title(reference)
    validate_year(reference)

    if reference['entry_type'] == "book":
        validate_book(reference)
    if reference['entry_type'] == "article":
        validate_article(reference)


def validate_author(reference):
    if 'author' not in reference or not reference['author'].strip():
        raise UserInputError("Author is required.")


def validate_title(reference):
    if len(reference['title']) < 2:
        raise UserInputError("Title must be at least 2 characters long.")

    if len(reference['title']) > 250:
        raise UserInputError("Title must be under 250 characters long.")


def validate_year(reference):
    if not reference['year'].isdigit() or not 1000 <= int(reference['year']) <= 9999:
        raise UserInputError("Year must be a valid 4-digit number between 1000 and 9999.")


def validate_book(reference):
    """Tarkastuksia 'book' viitetyypille"""
    if not reference['extra_fields'].get("publisher"):
        raise UserInputError("Publisher is required for books.")

def validate_article(reference):
    """Tarkastuksia 'article' viitetyypille"""
    if not reference['extra_fields'].get("journal"):
        raise UserInputError("Journal is required for articles.")


def generate_key(author, year, title):
    """Generoi viitteen citation key"""
    if not author or not title:
        raise UserInputError("Author and title are required to generate citation key.")
    surname = author.split(", ")[0]
    first_word = re.sub(r'[^a-zA-Z]', '', title.split()[0])
    return f"{surname}{year}{first_word}"
