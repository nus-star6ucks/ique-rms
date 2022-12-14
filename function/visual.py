"""
Includes all functions used to visualization
"""
import pandas as pd
import plotly.express as px
import os
from enum import Enum
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.bucket('ique-app-reports')
class UnitType(Enum):
    day = 12  # minium interval = 2 hours
    week = 7  # minium interval = day
    month = 5  # minium interval = week
    year = 13  # minium interval = year


unitValue = {'day': 12,
             'week': 7,
             'month': 5,
             'year': 13
             }

unitValueReverse = dict(zip(unitValue.values(), unitValue.keys()))

base_destination_path = "/reports/"
postfix = ".html"


def generate_url(type, data, unit, store, creattime):
    """
    generate diagram and return url to url-field
    :param type: report type
    :param data
    :param unit: to set the period in the diagram
    :param end: end value of Y
    :return url
    """
    allvaule = []

    ending = unit
    if unit is UnitType.year.value:
        ending -= 1
    for idx in range(0, ending):
        # extract data part
        allvaule += data['Period ' + str(idx + 1)]

    df = pd.DataFrame(allvaule)
    ChartTitle = "【" + store.name + "】 "

    if type == "AWT":
        secondD = "Average Wait Time"
        thirdD = "Seat Type"
        ChartTitle += secondD + " Report (" + unitValueReverse[unit] + ")"
        fig = px.line(df, x="Time", y=secondD, color=thirdD, title=ChartTitle, symbol=thirdD)  # line chart
        fig.update_layout(yaxis_title='Average Wait Time (s)')
    else:
        secondD = "Number"
        thirdD = "Status"
        ChartTitle += "People Number Report (" + unitValueReverse[unit] + ")"
        fig = px.bar(df, x="Time", y=secondD, color=thirdD, title=ChartTitle, barmode="group",
                     text_auto=True)  # bar chart
        fig.update_layout(yaxis_title='Number (person)')



    setView(type, fig, store, creattime)

    return base_destination_path + str(store.id) + "-" + str(creattime) + "-" + type + postfix


def setView(type, fig, store, creattime):
    """
    update and show diagram
    :param type: report type
    :param fig
    :param store:
    :param creattime:
    :return url
    """
    if type == 'AWT':
        fig.update_layout(
            xaxis=dict(
                showline=True,
                gridcolor='black',
                showgrid=False,
                showticklabels=True,
                linewidth=2,
                linecolor='black',
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=False,
                showline=False,
                linecolor='black',
                showticklabels=True,
            ),
            plot_bgcolor='white')
    else:
        fig.update_layout(
            xaxis=dict(
                showline=False,
                gridcolor='black',
                showgrid=False,
                showticklabels=True,
                titlefont_size=16,
                linewidth=2,
                linecolor='black',
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=False,
                showline=False,
                linecolor='black',
                showticklabels=True,
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            bargap=0.15,
            bargroupgap=0.1,
        )
        fig.update_traces(textfont_size=15, textfont_color='black', textangle=0, textposition="outside", cliponaxis=False)

    fig.show()

    filename = str(store.id) + "-" + str(creattime) + "-" + type + postfix

    file_path = filename
    fig.write_html(file_path)

    blob = bucket.blob('reports/' + filename)
    blob.upload_from_filename(file_path)

    os.remove(file_path)
