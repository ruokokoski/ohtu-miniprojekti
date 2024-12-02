from io import BytesIO
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, redirect, request, flash, jsonify, send_file
from db_helper import reset_db
from config import app, test_env
from repositories.search_handler import fetch_search_results
from repositories.reference_repository import (
    delete_reference,
    list_references_as_bibtex,
    list_references_as_dict,
    get_reference_by_key
)
from util import process_reference_form


@app.route("/")
def index():
    #references = get_references()
    return render_template("index.html")

@app.route("/new_reference")
def new():
    return render_template("new_reference.html")

@app.route('/create_reference', methods=['POST'])
def reference_creation():
    return process_reference_form(is_creation=True)

@app.route('/references')
def browse_references():
    references_dict = list_references_as_dict()
    return render_template('list_references.html', references=references_dict)

@app.route('/edit_reference/<citation_key>')
def edit_reference(citation_key):
    reference = get_reference_by_key(citation_key)
    print(reference)
    authors = reference.author.split(" and ")
    authors = [{"lastname":nimi.split(", ")[0] ,
                "firstnames":nimi.split(", ")[1] }
                for nimi in authors]
    print(authors)
    return render_template(
        'edit_reference.html',
        reference=reference,
        authors=authors,
        extra_fields=reference.extra_fields
        )


@app.route('/update_reference', methods=['POST'])
def update_reference_entry():
    citation_key = request.form.get('citation_key')
    if not citation_key:
        flash("Citation key is missing", "error")
        return redirect("/references")
    return process_reference_form(is_creation=False, citation_key=citation_key)

@app.route("/delete_reference/<citation_key>", methods=["POST"])
def reference_remove(citation_key):
    try:
        delete_reference(citation_key)
        flash("Reference deleted", "success")
    except ValueError as e:
        flash(f"Error: {str(e)}", "failure")
    except SQLAlchemyError as db_error:
        flash(f"Error when deleting reference: {str(db_error)}", "failure")
    return redirect("/references")

@app.route("/download")
def download_references():
    bibtex_data = list_references_as_bibtex()

    flash("Done", "success")

    # Muodostetaan tiedosto BytesIO-objektiksi, jotta se voidaan lähettää käyttäjälle
    return send_file(
        BytesIO(bytes(bibtex_data, "utf-8")),
        download_name="references.bib",
        as_attachment=True
    )

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_query = request.form.get("query", "")
        database = request.form.get("database", "ACM")
    else:
        search_query = request.args.get("query", "")
        database = request.args.get("database", "ACM")

    if not search_query:
        flash("Searchfield empty", "danger")
        return redirect("/")

    try:
        results = fetch_search_results(database, search_query)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect("/")
    '''
    if database == "ACM":
        results = fetch_acm_search_results(search_query)
    elif database == "Google Scholar":
        results = fetch_google_scholar_results(search_query)
    else:
        flash(f"Tuntematon tietokanta: {database}", "danger")
        return redirect("/")
    '''
    if results is None or len(results) == 0:
        flash("Search didn't find anything", "warning")
        return redirect("/")

    return render_template("index.html", results=results, database=database)

if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
