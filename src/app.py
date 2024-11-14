from flask import render_template#, redirect, request, jsonify, flash
#from db_helper import reset_db
from config import app#, test_env
#from repositories.reference_repository import list_references


@app.route("/")
def index():
    #references = get_references()
    return render_template("index.html")

@app.route("/new_reference")
def new():
    return render_template("new_reference.html")

# need to create db/table first..
#@app.route("/references")
#def browse_references():
    #references_list = list_references()
    #return render_template("list_references.html", references=references_list)
