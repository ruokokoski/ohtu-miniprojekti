from io import BytesIO
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, redirect, request, flash, jsonify, send_file
from db_helper import reset_db
from config import app, test_env
from repositories.reference_repository import (
    delete_reference,
    list_references_as_bibtex,
    list_references_as_dict,
    #get_bibtex,
    get_reference_by_key,
    update_reference
)
from entities.reference import Reference
from util import validate_reference, generate_key, UserInputError

@app.route("/")
def index():
    #references = get_references()
    return render_template("index.html")

@app.route("/new_reference")
def new():
    return render_template("new_reference.html")

@app.route('/create_reference', methods=['POST'])
def reference_creation():
    entry_type = request.form['entry_type']
    author = request.form['author']
    title = request.form['title']
    year = request.form['year']

    # Aloita dynaamisen extra_fields-datan luominen
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
        pass
        # Lisää muita kenttiä tarvittaessa

    # Luo Reference-objekti
    reference = Reference(
        entry_type=entry_type,
        citation_key=generate_key(author, year, title),
        author=author,
        title=title,
        year=year,
        extra_fields=extra_fields
    )

    try:
        validate_reference(reference)
        reference.save()
        flash("Uusi viite luotu onnistuneesti", "success")
        return redirect("/references")
    except UserInputError as error:
        flash(str(error), "failure")
        return redirect("/new_reference")

@app.route('/references')
def browse_references():
    references_dict = list_references_as_dict()
    return render_template('list_references.html', references=references_dict)

@app.route('/edit_reference/<reference_key>')
def edit_reference(reference_key):
    reference = get_reference_by_key(reference_key)
    authors = reference.author.split(" and ")
    authors = [{"sukunimi":nimi.split(", ")[0] ,
                "etunimi":nimi.split(", ")[1] }
                for nimi in authors]
    return render_template('edit_reference.html', reference=reference, authors=authors)

@app.route('/update_reference', methods=['POST'])
def update_reference_entry():
    data = {
        "key": request.form.get("key", ""),
        "author": request.form.get("author", ""),
        "year": request.form.get("year", ""),
        "title": request.form.get("title", ""),
        "publisher": request.form.get("publisher", ""),
        "address": request.form.get("address", ""),
        "volume": request.form.get("volume", ""),
        "series": request.form.get("series", ""),
        "edition": request.form.get("edition", ""),
        "month": request.form.get("month", ""),
        "note": request.form.get("note", ""),
        "url": request.form.get("url", "")
    }
    print(data)

    try:
        validate_reference(data)
        update_reference(data)
        flash("Viite päivitetty onnistuneesti", "success")
        return redirect("/references")

    except UserInputError as error:
        flash(str(error), "failure")
        return redirect(f"/edit_reference/{data['key']}")

@app.route("/delete_reference/<citation_key>", methods=["POST"])
def reference_remove(citation_key):
    try:
        delete_reference(citation_key)
        flash("Viite poistettu onnistuneesti", "success")
    except ValueError as e:
        flash(f"Virhe: {str(e)}", "failure")
    except SQLAlchemyError as db_error:
        flash(f"Virhe viitteen poistamisessa: {str(db_error)}", "failure")
    return redirect("/references")  


@app.route("/download")
def download_references():
    bibtex_data = list_references_as_bibtex()
    
    flash("Lataus onnistui", "success")

    # Muodostetaan tiedosto BytesIO-objektiksi, jotta se voidaan lähettää käyttäjälle
    return send_file(
        BytesIO(bytes(bibtex_data, "utf-8")),
        download_name="references.bib",       
        as_attachment=True                   
    )


if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
