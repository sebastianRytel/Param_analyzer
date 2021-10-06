# """Module for parsing PDF files with blood results. It extracting infromation such as date of
# test, results and LIMITS in which particular LIMITS should be within.
# """

import re
from typing import Dict, List
from datetime import datetime

import pdfplumber


class BloodResults:

    blood_parameters: List[str] = [
            "WBC",
            "NEU",
            "LYM",
            "MONO",
            "BASO",
            "EOS",
            "RBC",
            "HCT",
            "HGB",
            "MCV",
            "MCH",
            "MCHC",
            "PLT",
            "MPV",
            "PCT",
            "RET",
            "RET%",
            "IRF",
            "RDW",
            "RDW-SD",
        ]

    limits = {
        "WBC": [4, 10],
        "NEU": [2, 7],
        "LYM": [1, 3],
        "MONO": [0.2, 1],
        "BASO": [0, 0.2],
        "EOS": [0.05, 0.4],
        "RBC": [3.83, 5.1],
        "HCT": [34.5, 46.3],
        "HGB": [11.7, 15.5],
        "MCV": [80.4, 95.9],
        "MCH": [27.2, 33.5],
        "MCHC": [32.5, 35.2],
        "PLT": [150, 400],
        "MPV": [6.8, 11],
        "PCT": [0.19, 0.33],
        "RET": [0.02, 0.13],
        "RET_PERCENT": [0.2, 2.5],
        "IRF": [0.2, 0.4],
        "RDW": [11.7, 14.6],
        "RDW_SD": [36, 46],
    }

    units = {
        "WBC": "10´3/µl",
        "NEU": "10´3/µl",
        "LYM": "10´3/µl",
        "MONO": "10´3/µl",
        "BASO": "10´3/µl",
        "EOS": "10´3/µl",
        "RBC": "10´6/µl",
        "HCT": "%",
        "HGB": "g/dl",
        "MCV": "fl",
        "MCH": "pg",
        "MCHC": "g/dl",
        "PLT": "10´3/µl",
        "MPV": "fl",
        "PCT": "%",
        "RET": "10´6/µl",
        "RET_PERCENT": "%",
        "IRF": "%",
        "RDW": "%",
        "RDW_SD": "fl",
    }

    headers = (
        "DATE",
        "LAB_CODE",
        "WBC",
        "NEU",
        "LYM",
        "MONO",
        "BASO",
        "EOS",
        "RBC",
        "HCT",
        "HGB",
        "MCV",
        "MCH",
        "MCHC",
        "PLT",
        "MPV",
        "PCT",
        "RET",
        "RET_PERCENT",
        "IRF",
        "RDW",
        "RDW_SD",
    )

    def __init__(self):
        self.blood_results: Dict[str, float] = {
            param: None for param in self.blood_parameters
        }
        self.patient_name = None
        self.birth_date = None
        self.exam_date = None
        self.patient_id = None
        self.lab_code = None

    def extract_information(self, pdf_path: str) -> None:
        """
        1. Method opens one pdf defined by its path_uploads.
        2. Module pdfplumber iterates over the pdf, analyzing each line of the text.
        3. Separated methods are started in order to find required data using regex module.
        4. Each method are assigning values to value names defined in class constructor.
        5. At the end of this method, some of the data are stored into dictionary and are corrected,
        because of undesired
        extra characters.
        """
        with pdfplumber.open(pdf_path) as pdf:
            pages = pdf.pages[0]
            for text_line in pages.extract_text().splitlines():
                self.extract_date(text_line)
                self.extract_birth_date(text_line)
                self.extract_blood_parameters_data(text_line)
                self.extract_patient_name(text_line)
                self.get_lab_code(text_line)
        self.create_patient_id()

    def extract_birth_date(self, text_line: str) -> None:
        """
        Function extracts birth date from PDF file
        :param text_line: parsed_pdfs line of text
        :return: None
        """
        birth_date = re.search(r"ur\W+\d{4}-\d{2}-\d{2}\W+\d+\w+\W+\w+", text_line)
        if birth_date:
            self.birth_date = birth_date.group().split()[1].rstrip(",")

    def extract_blood_parameters_data(self, text_line: str) -> None:
        """
        Function tries to match each line to given regex definition. If success (True),
        parsed_pdfs line
        is passed to function which unify signatures (can be different for different
        laboratories). After unification, function filters from the whole list of parameters,
        only one which are required. Blood parameter and blood result is already split so those
        values are assigned directly to dictionary defined in __init__. Parsed text which is
        defining blood LIMITS in some cases is sticked to the UNITS. It is required to split those
        string, so next function pass parsed_pdfs text through two function for text normalization.
        After text normalization blood LIMITS and blood UNITS are assigned to dictionary defined
        in __init__.
        :param text_line: each line parsed_pdfs from PDF file.
        :return: None
        """

        blood_results = re.match(
            r"^[A-Z]{2,4}%?#?-?([A-Z]{2})?\s+\d+(.\d+)?", text_line
        )

        if blood_results:
            unified_parameter = self.unify_signature(blood_results)
            if unified_parameter in self.blood_results.keys():
                self.blood_results[unified_parameter] = float(
                    blood_results.group().split()[1]
                )

    def extract_date(self, text_line: str) -> None:
        """
        Function extracts exam date from PDF file.
        :param text_line: parsed_pdfs line of text
        :return: None
        """
        date = re.search(r"\d{2}-\d{2}-\d{4}", text_line)
        if date:
            self.exam_date = datetime.strptime(date.group(), "%d-%m-%Y").date()

    def extract_patient_name(self, text_line: str) -> None:
        """
        Function extract patient name.
        :param text_line: parsed_pdfs line of text
        :return: None
        """
        patient = re.search(
            r"Pacjent:\s[AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]+"
            r"\s[AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]+",
            text_line,
        )
        if patient:
            self.patient_name = " ".join((patient.group().split()[1:3]))

    def unify_signature(self, blood_result) -> str:
        """
        takes blood signature and unify its name as per unified signature dict
        {deviation : unified}.
        :param blood_result: one line of text parsed_pdfs from PDF. It contains signature,
        blood result,
        limit values and
        blood unit.
        :return: changed name of signature as stated in unified signatures
        """
        unified_signatures = {
            "EO": "EOS",
            "EOS#": "EOS",
            "EO%": "EOS%",
            "LYM#": "LYM",
            "MO": "MONO",
            "MONO#": "MONO",
            "BASO#": "BASO",
            "NEU#": "NEU",
            "NE": "NEU",
        }
        if blood_result.group().split()[0] in unified_signatures.keys():
            return unified_signatures.get(blood_result.group().split()[0])
        return blood_result.group().split()[0]

    def create_patient_id(self) -> None:
        """
        Function creates patient ID number using numbers from birth date and numbers converted
        from patient name using ASCII table. Next all numbers are summed up.
        :return: None
        """
        birth_date_to_numbers = [int(x) for x in self.birth_date if x.isdigit()]
        patient_name_to_numbers = [ord(x) for x in self.patient_name]
        birth_and_name_sum = sum(birth_date_to_numbers) + sum(
            list(patient_name_to_numbers)
        )
        self.patient_id = f"ID_{birth_and_name_sum}"

    def get_lab_code(self, text_line) -> None:
        """
        Function reads proper allowable lab code present in PDF file. It is further used to
        insert into database and dataframe.
        :param text_line: Parsed line of text.
        :return: None
        """
        allowable_lab_codes = ["BKK-M2", "BKK-M3", "MORF5", "MORF-P", "MORF[+]R"]
        lab_code = re.findall("|".join(allowable_lab_codes), text_line)
        if lab_code:
            self.lab_code = lab_code[0]

    def reset_attributes(self) -> None:
        """
        Function resets all class attributes. It is required to avoid wrong results assignment
        when program is running and PDFs are analyzed in the loop.
        :return: None
        """
        atrributes_dict = vars(self)
        atrributes_dict["blood_results"] = {param: None for param in self.blood_parameters}
