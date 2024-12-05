from io import BytesIO
from urllib.parse import quote, unquote
from sqlalchemy.exc import SQLAlchemyError

from flask import (render_template, redirect, request, flash, jsonify, send_file,
                   session, Response, url_for)

from db_helper import reset_db
from config import app, test_env
from repositories.search_handler import fetch_search_results, fetch_bibtex
from repositories.reference_repository import (
    delete_reference,
    list_references_as_bibtex,
    list_references_as_dict,
    get_reference_by_key,
    bibtex_to_dict
)
from util import process_reference_form
from entities.reference import Reference

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_reference")
def new():
    field_profiles = Reference.FIELD_PROFILES
    return render_template("new_reference.html", field_profiles=field_profiles)

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
    authors = reference.author.split(" and ")
    authors = [{"lastname":nimi.split(", ")[0] ,
                "firstnames":nimi.split(", ")[1] }
                for nimi in authors]
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

@app.route("/download", methods=["GET"])
def download_file():
    bibtex_data = list_references_as_bibtex()
    return send_file(
        BytesIO(bytes(bibtex_data, "utf-8")),
        download_name="references.bib",
        as_attachment=True
    )

@app.route("/download", methods=["POST"])
def download_references():
    return jsonify({
        "message": "Your BibTeX references file is ready for download.",
        "status": "success"
    })

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
    if results is None or len(results) == 0:
        flash("Search didn't find anything", "warning")
        return redirect("/")

    session['search_results'] = results

    return render_template("index.html", results=results, database=database)

@app.route("/bibtex/<int:result_id>", methods=["GET", "POST"])
def get_bibtex(result_id):
    print(f"Button pressed with result_id: {result_id}\n")
    search_results = session.get('search_results')
    if not search_results:
        return jsonify({"error": "No search results found in session"}), 404

    try:
        doi_link = search_results[result_id]["doi_link"]
        bibtex_data = fetch_bibtex(doi_link)
    except (IndexError, KeyError):
        return jsonify({"error": "Invalid result_id or BibTeX data not available"}), 404
    print(f"BibTeX data: {bibtex_data}")

    if request.method == "POST":
        encoded_bibtex = quote(bibtex_data)
        redirect_url = url_for("from_search_new_reference", bibtex=encoded_bibtex)
        print(f"Redirecting to: {redirect_url}")
        return redirect(redirect_url)

    return jsonify({"bibtex": bibtex_data}), 200

@app.route("/popup_new_search_reference", methods=["GET", "POST"])
def from_search_new_reference():
    bibtex = request.args.get('bibtex')
    print(f'Bibtex in popup route: {bibtex}')
    bibtex_decoded = unquote(bibtex)
    print(f'Decoded in popup route: {bibtex_decoded}')
    if not bibtex:
        return "No BibTeX data received.", 400
    
    if request.method == "POST":
        return process_reference_form(is_creation=True)

    reference = bibtex_to_dict(bibtex_decoded)
    print(f'reference: {reference}')
    entry_type = reference['entry_type']
    field_profiles = Reference.FIELD_PROFILES
    print(f'entry_type: {entry_type}\nfield_profiles: {field_profiles}')

    if not entry_type or entry_type not in field_profiles:
        error_message = (
            f"{entry_type.capitalize()} is unknown entry type. "
            "Please add the reference manually."
        )
        return render_template("popup_new_search_reference.html",
                               reference=reference,
                               entry_type=entry_type,
                               fields=field_profiles,
                               error_message=error_message)

    return render_template("popup_new_search_reference.html",
        reference=reference,
        entry_type=entry_type,
        fields=field_profiles
    )

if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
