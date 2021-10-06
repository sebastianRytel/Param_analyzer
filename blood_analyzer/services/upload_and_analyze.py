# PSL
from os import path, listdir
from typing import NoReturn

# Third part
from flask import flash, redirect, request

# Own
from blood_analyzer.services.openpdf import PATH_UPLOAD
from blood_analyzer.services import openpdf
from blood_analyzer.services import PATIENT
from blood_analyzer.db.models import Patients


def upload_pdf_file(pdf_file) -> NoReturn:
    if not pdf_file.filename or pdf_file.filename.rsplit(".")[1] != "pdf":
        flash("File is not PDF file or You didn't choose a PDF file", "danger")
    else:
        pdf_file.save(path.join(PATH_UPLOAD, pdf_file.filename))
        flash(f"You have uploaded {pdf_file.filename} file", "success")
    return redirect(request.url)


def analyze_pdf_file() -> NoReturn:
    list_of_files = [file for file in listdir(PATH_UPLOAD) if file.endswith("pdf")]
    if list_of_files:
        before_upload = Patients.query.count()
        openpdf.analyze_and_save_to_database(list_of_files)
        if not verify_data_in_pdf():
            return redirect(request.url)
        after_upload = Patients.query.count()
        flash_messsages(before=before_upload, after=after_upload, files=list_of_files)
    else:
        flash("File is not PDF file or You didn't choose a PDF file", "danger")
    return redirect(request.url)

def verify_data_in_pdf():
    if PATIENT.lab_code is None:
        flash("Some of the values has not been correctly recognized. Most probably lab code "
              "cannot be recognized ", "danger")
        return False
    return True

def flash_messsages(before, after, files):
    if before == after:
        flash(f"""
{files} have been analyzed and result has been added to already existing patient:
{PATIENT.patient_id}""", "success")
    else:
        flash(f"""
{files} have been analyzed. New patient has been added. New Patient ID is
{PATIENT.patient_id}""", "success")