from flask import render_template#, redirect, request, jsonify, flash
#from db_helper import reset_db
from config import app#, test_env

@app.route("/")
def index():
    #references = get_references()
    return render_template("index.html")

@app.route("/new_reference")
def new():
    return render_template("new_reference.html")
