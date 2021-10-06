"""
Shows matplot graphs on html page.
"""

from io import BytesIO
from typing import Any

import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates

from ..db.models import Results
from ..services import BloodResults


def plotting_graphs(parameter, patient_id, patient_age) -> Any:
    """
    Function creates graphs showing how blood parameter changes in function of time.
    :param parameter: Blood parameter used for LIMITS definition.
    :param df_series: Dataframe series for specific blood parameter.
    :param units: Blood parameter unit to show in graphs title.
    :return:
    """
    results_particular_parameter = Results.query.filter_by(
        patient_id=patient_id
    ).order_by(Results.DATE)
    result_to_graph = [
        result.__getattribute__(parameter) for result in results_particular_parameter
    ]
    results_dates = Results.query.filter_by(patient_id=patient_id).order_by(
        Results.DATE
    )
    results_dates_to_graph = [result.DATE for result in results_dates]
    plt.figure(figsize=(16, 10))
    plt.plot_date(
        results_dates_to_graph,
        result_to_graph,
        label="parameter value",
        linestyle="solid",
    )
    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter("%Y-%m-%d")
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gca().xaxis.set_major_locator(mpl_dates.MonthLocator())
    # patient.blood_limits is in format in example[[150.0, 400.0], '10´3/µl'].Lower and Upper limit
    # together with blood unit.
    plt.plot(
        results_dates_to_graph,
        [BloodResults.limits[parameter][1]] * len(result_to_graph),
        label="upper limit",
    )
    # Upper limit plotted on graph
    plt.plot(
        results_dates_to_graph,
        [BloodResults.limits[parameter][0]] * len(result_to_graph),
        label="lower limit",
    )  # Lower limit plotted on graph
    plt.legend(loc="upper right")
    plt.title(
        f"Patient age: {patient_age}\n"
        f"Parameter: {parameter} ({BloodResults.units.get(parameter)})"
    )
    plt.grid()
    plt.setp(plt.xticks()[1], rotation=30, ha="right")
    img = BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)
    return img
