"""
Initializing module for finding pdf files in static/uploads folder. It checks found PDF
file and creates class instance where all important data is extracted. Finally function saves
this data in database. After this parsed file is moved to static/parsed_pdfs folder.
"""

from os import path, remove
from typing import NoReturn

from blood_analyzer.services import PATIENT
from blood_analyzer import _STATIC_FOLDER
from blood_analyzer.db import add_to_database

PATH_UPLOAD: str = f"{_STATIC_FOLDER}/"


def open_parse_write_to_database(file_name: str) -> NoReturn:
    """
    Function initialize extract information on patient instance. Next writes all gathered data in
    database.

    :param file_name: name of the file found in uploads folder.
    :type file_name: str
    :return: None
    """
    PATIENT.extract_information(file_name)
    add_to_database.add_patient_result_to_database()


def delete_parsed_pdf(path_upload: str, file_name: str) -> NoReturn:
    """
    Function removes PDF file which were parsed.

    :return: None
    """
    src_path = path.join(path_upload, file_name)
    remove(src_path)


def analyze_and_save_to_database(list_of_files) -> NoReturn:
    """
    Function get all files gathered by look_for_pdf function, next if any file is present it
    opens file, parse and write to DB. Next parsed file is moved to different folder. Finally
    blood results attribute is reset.

    :return: boolean. It is required to recognize action in routes module.
    :rtype: None
    """
    for file in list_of_files:
        open_parse_write_to_database(path.join(PATH_UPLOAD, file))
        delete_parsed_pdf(PATH_UPLOAD, file)
        PATIENT.reset_attributes()
