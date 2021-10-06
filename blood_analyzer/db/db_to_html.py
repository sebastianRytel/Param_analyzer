from datetime import datetime

from blood_analyzer.db.get_from_database import jsonify_database_objects
from blood_analyzer.db.models import Patients


def write_db_data_to_html(patient_id):
    birth_date = Patients.query.filter_by(patient_id=patient_id).first()
    birth_date_year = str(birth_date.birth_date).split("-")[0]
    current_time_year = str(datetime.now()).split("-")[0]
    age = int(current_time_year) - int(birth_date_year)
    results_from_db = jsonify_database_objects(patient_id)
    return age, patient_id, results_from_db


def get_patients_from_db():
    return [patient.patient_id for patient in Patients.query.all()]
