from io import BytesIO
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, redirect, request, flash, jsonify, send_file
from db_helper import reset_db
from config import app, test_env
from repositories.reference_repository import (
    list_references,
    create_reference,
    delete_reference,
    #get_bibtex,
    list_references_as_bibtex,
    get_reference_by_key,
    update_reference
)
from util import validate_reference, generate_key, UserInputError



@app.route("/")
def index():
    #references = get_references()
    return render_template("index.html")

@app.route("/new_reference")
def new():
    return render_template("new_reference.html")


@app.route("/references")
def browse_references():
    #testi bibtexin hakuun:
    #bibtex_data = get_bibtex()
    references_list = list_references()
    return render_template("list_references.html",
                           references=references_list,
    )

@app.route("/create_reference", methods=["POST"])
def reference_creation():
    data = {
        #required
        "author": request.form.get("author", ""),
        "year": request.form.get("year", ""),
        "title": request.form.get("title", ""),
        "publisher": request.form.get("publisher", ""),
        "type": request.form.get("type", ""),
        #optional
        "address": request.form.get("address", ""),
        "volume": request.form.get("volume", ""),
        "series": request.form.get("series", ""),
        "edition": request.form.get("edition", ""),
        "month": request.form.get("month", ""),
        "note": request.form.get("note", ""),
        "url": request.form.get("url", ""),
        "number": request.form.get("number", ""),
    }

    # Korvataan tyhjät kentät tyhjällä merkkijonolla
    for key, value in data.items():
        if value == "":
            data[key] = ""  # Varmistetaan, että kenttä on tyhjä merkkijono

    data["key"] = generate_key(data["author"], data["year"], data["title"])

    try:
        validate_reference(data)
        create_reference(data)
        flash("Uusi viite luotu onnistuneesti", "success")
        return redirect("/references")

    except UserInputError as error:
        flash(str(error), "failure")
        return redirect("/new_reference")

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
    # Korvataan tyhjät kentät tyhjällä merkkijonolla
    for key, value in data.items():
        if value == "":
            data[key] = ""  # Varmistetaan, että kenttä on tyhjä merkkijono

    try:
        validate_reference(data)
        update_reference(data)
        flash("Viite päivitetty onnistuneesti", "success")
        return redirect("/references")

    except UserInputError as error:
        flash(str(error), "failure")
        return redirect(f"/edit_reference/{data['key']}")


@app.route("/delete_reference/<key>", methods=["POST"])
def reference_remove(key):
    try:
        delete_reference(key)
        flash("Viite poistettu onnistuneesti", "success")
    except SQLAlchemyError as db_error:
        flash(f"Virhe viitteen poistamisessa: {str(db_error)}", "failure")
    return redirect("/references")

@app.route("/download")
def download_references():
    bibtex_data = list_references_as_bibtex()

    # Muodostetaan tiedosto BytesIO-objektiksi, jotta se voidaan lähettää käyttäjälle
    return send_file(
        BytesIO(bytes(bibtex_data, "utf-8")),  # Muutetaan BibTeX-teksti byteiksi
        download_name="references.bib",       # Lataustiedoston nimi
        as_attachment=True                   # Varmistaa, että tiedosto ladataan
    )


if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
