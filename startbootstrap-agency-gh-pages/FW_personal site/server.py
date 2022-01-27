from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf import CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email
from smtplib import SMTP
from flask_sqlalchemy import SQLAlchemy
import os
import email_validator


MAIL = "fwimpf@gmail.com"
PASSWORD = "aq)fq2:eD8X_B+"
SECRET_KEY = os.urandom(20)

app = Flask(__name__)

csrf = CSRFProtect(app)
csrf.init_app(app)
Bootstrap(app)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///experience.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# PATH = "static/assets/portfolio_files"


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(250), nullable=False)
    timespan = db.Column(db.String(250), nullable=True)
    header = db.Column(db.String(250), nullable=False)
    short_description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(250), nullable=True)
    icon_size = db.Column(db.String(250), nullable=True)
    article = db.Column(db.Text, nullable=True)
    reference_one = db.Column(db.String(250), nullable=True)
    reference_two = db.Column(db.String(250), nullable=True)
    reference_three = db.Column(db.String(250), nullable=True)
    reference_four = db.Column(db.String(250), nullable=True)
    image = db.Column(db.String(250), nullable=True)
    modal = db.Column(db.String(250), nullable=True)
    timeline_direction = db.Column(db.String(250), nullable=True)
    image_two = db.Column(db.String(250), nullable=True)
    github_link = db.Column(db.String(250), nullable=True)


class MyForm(FlaskForm):
    name = StringField(label="Name",
                       validators=[InputRequired("Please enter a name.")])
    mail = StringField(label="Your E-Mail-Address",
                       validators=[InputRequired("Please enter an Email address."),
                                   Email(message="Please enter a valid Email.")])
    subject = StringField(label="Subject",
                          validators=[InputRequired("please enter a subject.")])
    body = TextAreaField(label="Message",
                         validators=[InputRequired("Please enter a message.")])
    submit = SubmitField(label="Send Mail")


db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    experience_data = Experience.query.filter(Experience.topic == "experience")
    portfolio_data = Experience.query.filter(Experience.topic == "portfolio")
    education_data = Experience.query.filter(Experience.topic == "education")
    skill_data = Experience.query.filter(Experience.topic == "skills")
    contact_form = MyForm()
#     directory = os.fsencode(PATH)
#     filenames = [str(os.fsencode(file)).split(".")[0] for file in os.listdir(directory)]
#     filenames = sorted(filenames, key=str.lower)
    if contact_form.validate_on_submit():
        name = contact_form.name.data
        mail = contact_form.mail.data
        subject = contact_form.subject.data
        text = contact_form.body.data
        connection = SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=MAIL, password=PASSWORD)
        connection.sendmail(from_addr=MAIL, to_addrs=MAIL, msg=f"Subject:{subject}\n\nfrom {name}\n"
                                                               f"Email: {mail}\n\n{text}")
        return redirect(url_for("home", form=contact_form, exp_db=experience_data, port_db=portfolio_data,
                                edu_db=education_data, skill_db=skill_data))
    return render_template("index.html", form=contact_form, exp_db=experience_data, port_db=portfolio_data,
                           edu_db=education_data, skill_db=skill_data)


@app.route("/experience/<header>", methods=["Get", "POST"])
def experience(header):
    experience_data = Experience.query.filter(Experience.topic == "experience")
    return render_template("experience.html", header=header, exp_db=experience_data)


if __name__ == "__main__":
    app.run(debug=True)
