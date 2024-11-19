from flask import render_template, redirect, request, flash, jsonify, send_file
from db_helper import reset_db
from config import app, test_env
from repositories.reference_repository import list_references, create_reference
from util import validate_reference, UserInputError
from io import BytesIO


@app.route("/")
def index():
    #references = get_references()
    return render_template("index.html")

@app.route("/new_reference")
def new():
    return render_template("new_reference.html")


@app.route("/references")
def browse_references():
    references_list = list_references()
    return render_template("list_references.html", references=references_list)

@app.route("/create_reference", methods=["POST"])
def reference_creation():

    data = {
        #"reference_type": request.form.get("reference_type"),
        "key": request.form.get("citation_key"),
        "author": request.form.get("author"),
        "year": request.form.get("year"),        
        "title": request.form.get("title"),
        "publisher": request.form.get("publisher"),
        "address": request.form.get("address")
    }

    try:
        validate_reference(data)
        create_reference(data)
        flash("Uusi viite luotu onnistuneesti")
        return redirect("/")

    except UserInputError as error:
        flash(str(error))
        return redirect("/new_reference")


@app.route("/download")
def download_references():
    test_data = "esimerkki referenssi"
    return send_file(BytesIO(bytes(test_data, "utf-8")), download_name="references.bib", as_attachment=True)


if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
