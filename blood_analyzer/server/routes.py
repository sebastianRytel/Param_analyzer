"""
Module is used for representing data on web page and requests for important data.
"""
import ast

from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user, login_required

# __init__
from blood_analyzer import _BCRYPT, _DB

# My database services
from blood_analyzer.db.models import User
from blood_analyzer.db.db_to_html import write_db_data_to_html, get_patients_from_db

# My services
from blood_analyzer.services import BloodResults
from blood_analyzer.services.login import login_to_app
from blood_analyzer.services.register import register_to_app
from blood_analyzer.services.reset_token import reset_password
from blood_analyzer.services.reset_request import send_mail_with_reset
from blood_analyzer.services.show_graph import show_graph_on_page
from blood_analyzer.services.to_excel import save_table_as_excel
from blood_analyzer.services.upload_and_analyze import analyze_pdf_file, upload_pdf_file

# My server services
from blood_analyzer.server.forms import (RegistrationForm, LoginForm, RequestResetForm,
                                         ResetPasswordForm)

from . import SERVER_BLUEPRINTS


@SERVER_BLUEPRINTS.route("/")
@login_required
def home():
    return render_template("home.html", title="Home page")


@SERVER_BLUEPRINTS.route("/graph", methods=["POST"])
@login_required
def graph():
    """
    Function creates graph on web page.
    :return: Image of graph.
    """
    return show_graph_on_page(parameter=request.form["param"])


@SERVER_BLUEPRINTS.route("/excel", methods=["POST"])
@login_required
def excel():
    """
    Function saves dataframe as excel file.
    :return: rendered template
    """
    patient_id = request.form["excel"].split("|")[0].strip()
    results = request.form["excel"].split("|")[1].strip()
    save_table_as_excel(patient_id=patient_id, results=ast.literal_eval(results))
    return render_template("excel.html", title="Export to Excel", patient_id=patient_id)


@SERVER_BLUEPRINTS.route("/login", methods=["GET", "POST"])
def login():
    """
    Function creates login form.
    :return: rendered template
    """
    form = LoginForm()
    login_requirements = _BCRYPT, form, flash, login_user
    if current_user.is_authenticated:
        return redirect(url_for("server.home"))
    if form.validate_on_submit():
        login_to_app(login_requirements)
        return redirect(url_for("server.home"))
    return render_template("login.html", title="Login", form=form)


@SERVER_BLUEPRINTS.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("server.login"))


@SERVER_BLUEPRINTS.route("/patients", methods=["GET", "POST"])
@login_required
def patients():
    """
    Function creates table with results, buttons which allows to show graph and export to excel
    button.
    :return: web page
    """
    patients_id = get_patients_from_db()
    if request.method == "GET":
        return render_template(
            "patients.html",
            patients=patients_id,
            title="Patients List",
        )
    elif request.method == "POST":
        return redirect(url_for("tables"))


@SERVER_BLUEPRINTS.route("/register", methods=["GET", "POST"])
def register():
    """
    Function creates registration form.
    :return:
    """
    form = RegistrationForm()
    register_requirements = _BCRYPT, form, redirect, flash, url_for
    if current_user.is_authenticated:
        return redirect(url_for("server.home"))
    if form.validate_on_submit():
        register_to_app(register_requirements,
                        server_login="server.login")
    return render_template("register.html", title="Register", form=form)


@SERVER_BLUEPRINTS.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    form = RequestResetForm()
    reset_requirements =  User, form, flash
    if current_user.is_authenticated:
        return redirect(url_for("server.home"))
    if form.validate_on_submit():
        send_mail_with_reset(reset_requirements,
                             server_reset_token="server.reset_token")
        return redirect(url_for("server.login"))
    return render_template("reset_request.html", title='Reset Password', form=form)


@SERVER_BLUEPRINTS.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    form = ResetPasswordForm()
    reset_requirements = _BCRYPT, _DB, form, flash
    if current_user.is_authenticated:
        return redirect(url_for("server.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is invalid or expired token.", "warning")
        return redirect(url_for("server.reset_request"))
    if form.validate_on_submit():
        reset_password(reset_requirements, user=user)
        return redirect(url_for("server.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)


@SERVER_BLUEPRINTS.route("/tables", methods=["GET", "POST"])
@login_required
def tables():
    age, patient_id, results_from_db = write_db_data_to_html(patient_id=request.form["patient"])
    return render_template(
        "tables.html",
        headers=BloodResults.headers,
        results=results_from_db,
        limits=BloodResults.limits,
        patient_id=patient_id,
        age=age,
        parameters=list(BloodResults.headers)[2:],
    )


@SERVER_BLUEPRINTS.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """
    Function allows to upload PDF files and save then in static folder.
    :return:
    """
    if request.method == "POST":
        if request.files:
            upload_pdf_file(pdf_file=request.files["pdf"])
        elif request.form["analyze"]:
            analyze_pdf_file()
    return render_template("upload.html", title="Upload PDF File")
