from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()], render_kw={"autofocus": True, "autocomplete": 'off'})
    location = StringField('Cafe Location', validators=[DataRequired()], render_kw={"autocomplete": 'off'})
    map_url = StringField('Cafe location on Google maps (URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    seats = StringField("Number of seats?", validators=[DataRequired()])
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    has_sockets = SelectField("Has sockets?", choices=["Yes", "No"])
    has_toilet = SelectField("Has toilet?", choices=["Yes", "No"])
    has_wifi = SelectField("Has wifi?", choices=["Yes", "No"])
    can_take_calls = SelectField("Can take calls?", choices=["Yes", "No"])
    submit = SubmitField('Add')


def convert_to_bool(answer):
    if answer == "Yes":
        return True
    else:
        return False


@app.route("/")
def home():
    all_cafes = Cafe.query.all()
    return render_template("index.html", cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.cafe.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=convert_to_bool(form.has_sockets.data),
            has_toilet=convert_to_bool(form.has_toilet.data),
            has_wifi=convert_to_bool(form.has_wifi.data),
            can_take_calls=convert_to_bool(form.can_take_calls.data),
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add-cafe.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
