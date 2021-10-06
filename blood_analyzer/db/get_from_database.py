"""
Module is used for creating marshmallow object which contains result table get from database.
Function jsonify_database_object creates instance of marshmallow object and allows to transform
queried data to json object. Next after sorting by proper column order function returns list of
dictionaries which is used for showing it in flask app.
"""

from typing import List, Dict

from blood_analyzer import _MARSH
from blood_analyzer.db.models import Results
from blood_analyzer.services import BloodResults


class ResultsSchema(_MARSH.Schema):
    """
    Schema for creating field for json object
    """

    class Meta:
        fields = BloodResults.headers


def jsonify_database_objects(patient_id) -> List:
    """
    Function
    :param patient_id:
    :return:
    """
    proper_order = list(BloodResults.headers)
    sorted_results: List[Dict[str, float]] = []
    results_schema = ResultsSchema(many=True)
    results = Results.query.filter_by(patient_id=patient_id).order_by(Results.DATE)
    json_results = results_schema.jsonify(results).json
    for results in json_results:
        sorted_results.append({column: results[column] for column in proper_order})
    return sorted_results
