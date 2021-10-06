from typing import NoReturn

from sqlalchemy import exc

from blood_analyzer import _DB
from blood_analyzer.services import PATIENT
from blood_analyzer.db.models import Patients, Results


def add_patient_result_to_database() -> NoReturn:
    patient_in_db = Patients.query.filter_by(patient_id=PATIENT.patient_id).first()
    if patient_in_db:
        try:
            new_results = Results(
                patient_id=patient_in_db.patient_id,
                LAB_CODE=PATIENT.lab_code,
                DATE=PATIENT.exam_date,
                WBC=PATIENT.blood_results.get("WBC"),
                NEU=PATIENT.blood_results.get("NEU"),
                LYM=PATIENT.blood_results.get("LYM"),
                MONO=PATIENT.blood_results.get("MONO"),
                BASO=PATIENT.blood_results.get("BASO"),
                EOS=PATIENT.blood_results.get("EOS"),
                RBC=PATIENT.blood_results.get("RBC"),
                HCT=PATIENT.blood_results.get("HCT"),
                HGB=PATIENT.blood_results.get("HGB"),
                MCV=PATIENT.blood_results.get("MCV"),
                MCH=PATIENT.blood_results.get("MCH"),
                MCHC=PATIENT.blood_results.get("MCHC"),
                PLT=PATIENT.blood_results.get("PLT"),
                MPV=PATIENT.blood_results.get("MPV"),
                PCT=PATIENT.blood_results.get("PCT"),
                RET=PATIENT.blood_results.get("RET"),
                RET_PERCENT=PATIENT.blood_results.get("RET%"),
                IRF=PATIENT.blood_results.get("IRF"),
                RDW=PATIENT.blood_results.get("RDW"),
                RDW_SD=PATIENT.blood_results.get("RDW-SD"),
            )
            _DB.session.add(new_results)
            _DB.session.commit()
        except exc.IntegrityError:
            _DB.session.rollback()
    else:
        new_patient = Patients(
            patient_id=PATIENT.patient_id, birth_date=PATIENT.birth_date
        )
        _DB.session.add(new_patient)
        _DB.session.commit()
        new_results = Results(
            patient_id=PATIENT.patient_id,
            LAB_CODE=PATIENT.lab_code,
            DATE=PATIENT.exam_date,
            WBC=PATIENT.blood_results.get("WBC"),
            NEU=PATIENT.blood_results.get("NEU"),
            LYM=PATIENT.blood_results.get("LYM"),
            MONO=PATIENT.blood_results.get("MONO"),
            BASO=PATIENT.blood_results.get("BASO"),
            EOS=PATIENT.blood_results.get("EOS"),
            RBC=PATIENT.blood_results.get("RBC"),
            HCT=PATIENT.blood_results.get("HCT"),
            HGB=PATIENT.blood_results.get("HGB"),
            MCV=PATIENT.blood_results.get("MCV"),
            MCH=PATIENT.blood_results.get("MCH"),
            MCHC=PATIENT.blood_results.get("MCHC"),
            PLT=PATIENT.blood_results.get("PLT"),
            MPV=PATIENT.blood_results.get("MPV"),
            PCT=PATIENT.blood_results.get("PCT"),
            RET=PATIENT.blood_results.get("RET"),
            RET_PERCENT=PATIENT.blood_results.get("RET%"),
            IRF=PATIENT.blood_results.get("IRF"),
            RDW=PATIENT.blood_results.get("RDW"),
            RDW_SD=PATIENT.blood_results.get("RDW-SD"),
        )
        _DB.session.add(new_results)
        _DB.session.commit()
