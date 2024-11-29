import re
from flask import redirect, request, flash
from entities.reference import Reference
from repositories.reference_repository import get_reference_by_key
from exceptions import UserInputError


def process_reference_form(is_creation, citation_key=None):
    """Käsittelee lomakkeen tiedot ja suorittaa validoinnin."""
    # Haetaan formista lähetetyt tiedot
    entry_type = request.form.get('entry_type', 'book')
    author = request.form.get('author', '')
    title = request.form.get('title', '')
    year = request.form.get('year', '')

    # Luodaan extra_fields dynaamisesti
    extra_fields = create_extra_fields(entry_type)

    # Luo data-sanakirja
    data = {
        "entry_type": entry_type,
        "author": author,
        "title": title,
        "year": year,
        "extra_fields": extra_fields
    }

    if not is_creation and citation_key:
        data['citation_key'] = citation_key  # Lisätään citation_key dataan

    # Suoritetaan validointi
    try:
        validate_reference(data)

        # Luo uusi viite tai päivitä olemassa oleva
        if is_creation:
            create_reference(data)
            flash("Uusi viite luotu onnistuneesti", "success")
        else:
            update_reference(citation_key, data)
            flash("Viite päivitetty onnistuneesti", "success")

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
    if entry_type == "book":
        extra_fields["publisher"] = request.form.get('publisher', '')
        extra_fields["address"] = request.form.get('address', '')
        extra_fields["volume"] = request.form.get('volume', '')
        extra_fields["series"] = request.form.get('series', '')
        extra_fields["edition"] = request.form.get('edition', '')
        extra_fields["month"] = request.form.get('month', '')
        extra_fields["note"] = request.form.get('note', '')
        extra_fields["url"] = request.form.get('url', '')
        extra_fields["isbn"] = request.form.get('isbn', '')
    elif entry_type == "article":
        pass  # Lisää kentät artikkeleille, jos tarpeen
    return extra_fields


def create_reference(data):
    """Luo uusi viite ja tallenna se tietokantaan"""
    reference = Reference(
        entry_type=data['entry_type'],
        citation_key=generate_key(data['author'], data['year'], data['title']),
        author=data['author'],
        title=data['title'],
        year=data['year'],
        extra_fields=data['extra_fields']
    )
    reference.save()  # Tallenna uusi viite


def update_reference(citation_key, data):
    """Päivitä olemassa oleva viite"""
    reference = get_reference_by_key(citation_key)  # Hakee viitteen tietokannasta
    reference.update(data)  # Päivittää viitteen


def validate_reference(reference):
    """Suorita yleinen validointi"""
    validate_author(reference)
    validate_title(reference)
    validate_year(reference)

    # Viitetyypin tarkastukset
    if reference['entry_type'] == "book":
        validate_book(reference)


def validate_author(reference):
    if not reference['author'] or len(reference['author'].strip()) == 0:
        raise UserInputError("Author is required.")


def validate_title(reference):
    if len(reference['title']) < 2:
        raise UserInputError("Title must be at least 2 characters long.")
    if len(reference['title']) > 100:
        raise UserInputError("Title must be under 100 characters long.")


def validate_year(reference):
    if not reference['year'].isdigit() or not 1000 <= int(reference['year']) <= 9999:
        raise UserInputError("Year must be a valid 4-digit number between 1000 and 9999.")


def validate_book(reference):
    """Tarkastuksia 'book' viitetyypille"""
    #if not reference['extra_fields'].get("publisher"):
    #    raise UserInputError("Publisher is required for books.")

    #if not reference['extra_fields'].get("isbn"):
    #    raise UserInputError("ISBN is required for books.")

    # Voit tarkistaa muita kenttiä, kuten address, edition, jne.
    #if len(reference['extra_fields'].get("isbn", "")) < 10:
    #    raise UserInputError("ISBN must be at least 10 characters long.")


def generate_key(author, year, title):
    """Generoi viitteen citation key"""
    if not author or not title:
        raise UserInputError("Author and title are required to generate citation key.")
    surname = author.split(", ")[0]
    first_word = re.sub(r'[^a-zA-Z]', '', title.split()[0])
    return f"{surname}{year}{first_word}"
