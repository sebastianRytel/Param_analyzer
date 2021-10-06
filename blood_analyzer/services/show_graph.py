from flask import send_file

from blood_analyzer.services import create_graph

def show_graph_on_page(parameter):
    parameter, patient_id, age = (
        parameter.split(",")[0],
        parameter.split(",")[1].strip(),
        parameter.split(",")[2].strip(),
    )
    graph_img = create_graph.plotting_graphs(
        parameter=parameter, patient_id=patient_id, patient_age=age
    )
    return send_file(graph_img, mimetype="image/png")
