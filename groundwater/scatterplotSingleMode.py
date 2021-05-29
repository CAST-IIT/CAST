import json
import plotly
import random

import pandas as pd
import plotly.graph_objs as go

from flask_login import current_user
from groundwater.dataStorage import user_database

df = pd.read_csv('groundwater/static/original.csv')
limit = df['Site No.'].size + 1

def generate_site_numbers(no_of_data):
    user_site_no = []
    for x in range(no_of_data):
        r = random.randint(1, limit)
        if r not in user_site_no:
            user_site_no.append(r)
    return user_site_no

def create_singlePlot(lMax):
    table_data = user_database(current_user.id)
    for col in df.columns:
            if df[col].dtype == 'float64':
                df[col] = df[col].round(4)
    plume_length = [item[4] for item in table_data]
    user_site_no = generate_site_numbers(len(plume_length))
    compound_names = [item[2] for item in table_data]
    chem_group_name = [item[13] for item in table_data]
    for (i,j) in zip(compound_names,chem_group_name):
        similar_data = df[(df['Compound'].str.lower() == i.lower()) & (df['Chem. Group'].str.lower()==j.lower())]
    if not compound_names:
        similar_data = []
        user_site_no_similar_data = []
    else:
        similar_data = similar_data['Plume length[m]'].to_numpy()
        user_site_no_similar_data = generate_site_numbers(len(similar_data))
    trace1 = go.Scatter(
        x=[df['Site No.'].size / 2],
        y=[lMax],
        name='Model <i>L<sub>Max</sub></i>',
        mode='markers',
        marker=dict(
            size=14,
            color='#003f5c'
        )
    )
    trace2 = go.Scatter(
        x=df['Site No.'],
        y=df['Plume length[m]'],
        mode='markers',
        name= 'Original Database Plume Length (<i>L<sub>Max</sub></i>)',
        marker=dict(
            size=14,
            color='#ffa600'
        )
    )
    trace3 = go.Scatter(
        x=user_site_no_similar_data,
        y=similar_data,
        mode='markers',
        name='Similar sites in original database (<i>L<sub>Max</sub></i>)',
        marker=dict(
            size=14,
            color='#FF6361'
        )
    )
    data = [trace1, trace2,trace3]
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
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
