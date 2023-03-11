from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, NumberRange, Length, URL


class AddPetForm(FlaskForm):
    """Form for adding a pet"""

    name = StringField("Pets Name:", validators=[
                       InputRequired('A name must be provided')])
    species = SelectField("What type of pet?:", choices=[
                          ("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")])
    photo_url = StringField('Upload picture of Pet:',
                            validators=[Optional(), URL()])
    age = IntegerField("What is the pets age in years?:",
                       validators=[Optional(), NumberRange(min=0, max=30)])
    notes = StringField("Anything to mention about pet?:",
                        validators=[Optional(), Length(min=10)])
    available = BooleanField("Has the pet been adopted?:",
                             validators=[Optional()])


class EditPetForm(FlaskForm):
    """Form to edit an existing pet."""

    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()],
    )

    notes = TextAreaField(
        "Comments",
        validators=[Optional(), Length(min=10)],
    )

    available = BooleanField("Available?")
