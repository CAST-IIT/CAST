import json

import matplotlib
import random
import plotly
import plotly.graph_objs as go

matplotlib.use('Agg')
import pandas as pd
df = pd.read_csv('groundwater/static/original.csv')
limit = df['Site No.'].size + 1


def generate_site_numbers(no_of_data):
    user_site_no = []
    for x in range(no_of_data):
        r = random.randint(1, limit)
        if r not in user_site_no:
            user_site_no.append(r)
    return user_site_no


def create_liedlPlotMultiple(siteList,table_data):
    modelPlumeLength = [item[6] for item in table_data]
    user_site_no = generate_site_numbers(len(modelPlumeLength))
    trace1 = go.Scatter(
        x=user_site_no,
        y=modelPlumeLength,
        name='Model Plume Length(LMax)',
        mode='markers',
        marker=dict(
            size=14,
            color='#ffa600'
        )
    )

    siteNum = []
    siteVal = []

    for siteNo in siteList:
        idx = df['Site No.'].tolist().index(siteNo)
        siteNum.append(int(df['Site No.'].values[idx]))
        siteVal.append(df['Plume length[m]'].values[idx])

    trace2 = go.Scatter(
        x=siteNum,
        y=siteVal,
        mode='markers',
        name='Field Plume Length(LMax)',
        marker=dict(
            size=14,
            color='#003f5c'
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        titlefont=dict(
            size=25
        ),
        legend={
            "xanchor": "right",
            "y": 1,
            "x": 1
        },
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            title='Site Number',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            title='Plume Length (m)',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def create_chuEtAlPlotMultiple(siteList, table_data):
    modelPlumeLength = [item[7] for item in table_data]
    user_site_no = generate_site_numbers(len(modelPlumeLength))
    trace1 = go.Scatter(
        x=user_site_no,
        y=modelPlumeLength,
        name='Model Plume Length(LMax)',
        mode='markers',
        marker=dict(
            size=14,
            color='#ffa600'
        )
    )
    siteNum = []
    siteVal = []

    for siteNo in siteList:
        idx = df['Site No.'].tolist().index(siteNo)
        siteNum.append(int(df['Site No.'].values[idx]))
        siteVal.append(df['Plume length[m]'].values[idx])

    trace2 = go.Scatter(
        x=siteNum,
        y=siteVal,
        mode='markers',
        name='Field Plume Length(LMax)',
        marker=dict(
            size=14,
            color='#003f5c'
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        titlefont=dict(
            size=25
        ),
        legend={
            "xanchor": "right",
            "y": 1,
            "x": 1
        },
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            title='Site Number',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            title='Plume Length (m)',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def create_HamPlotMultiple(siteList,table_data):
    modelPlumeLength = [item[5] for item in table_data]
    user_site_no = generate_site_numbers(len(modelPlumeLength))
    trace1 = go.Scatter(
        x=user_site_no,
        y=modelPlumeLength,
        name='Model Plume Length(LMax)',
        mode='markers',
        marker=dict(
            size=14,
            color='#ffa600'
        )
    )
    siteNum = []
    siteVal = []

    for siteNo in siteList:
        idx = df['Site No.'].tolist().index(siteNo)
        siteNum.append(int(df['Site No.'].values[idx]))
        siteVal.append(df['Plume length[m]'].values[idx])

    trace2 = go.Scatter(
        x=siteNum,
        y=siteVal,
        mode='markers',
        name='Field Plume Length(LMax)',
        marker=dict(
            size=14,
            color='#003f5c'
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        titlefont=dict(
            size=25
        ),
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        legend={
            "xanchor": "right",
            "y": 1,
            "x": 1
        },
        xaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def create_Liedl3DMultiple(siteList,table_data):
    modelPlumeLength = [item[9] for item in table_data]
    user_site_no = generate_site_numbers(len(modelPlumeLength))
    trace1 = go.Scatter(
        x=user_site_no,
        y=modelPlumeLength,
        name='Model Plume Length(LMax)',
        mode='markers',
        marker=dict(
            size=14,
            color='#ffa600'
        )
    )

    siteNum = []
    siteVal = []

    for siteNo in siteList:
        idx = df['Site No.'].tolist().index(siteNo)
        siteNum.append(int(df['Site No.'].values[idx]))
        siteVal.append(df['Plume length[m]'].values[idx])

    trace2 = go.Scatter(
        x=siteNum,
        y=siteVal,
        mode='markers',
        name='Field Plume Length(LMax)',
        marker=dict(
            size=14,
            color='#003f5c'
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        titlefont=dict(
            size=25
        ),
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        legend={
            "xanchor": "right",
            "y": 1,
            "x": 1
        },
        xaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

