"""Adoption Agency application."""

from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pet_adoption_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "adoptAllpets123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def pet_list():
    """homepage of adoption agency, shows pets"""
    pets = Pet.query.all()
    return render_template('pet_list.html', pets=pets)


@app.route('/add', methods=["GET", "POST"])
def add_pets():
    """create new pet form; handling adding"""
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data

        flash(f"added {name} the {species}")
        pet = Pet(name=name, species=species)
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('pet_list'))
    else:
        return render_template('pet_add_form.html', form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """Edit pet."""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('pet_list'))

    else:
        return render_template("pet_edit_form.html", form=form, pet=pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)
