from pandas import DataFrame, ExcelWriter
from blood_analyzer import _STATIC_FOLDER

def save_table_as_excel(patient_id, results):
    df = DataFrame(results)
    writer = ExcelWriter(f"{_STATIC_FOLDER}/{patient_id}.xlsx")
    df.to_excel(writer)
    writer.save()
