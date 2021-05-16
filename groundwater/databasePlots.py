import json
import random
import scipy.stats as ss
from scipy.stats import norm
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import plotly.tools as tls
import plotly
import plotly.graph_objs as go
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


def create_bargraph(table_data):
    # original = siteUnit[:112]
    # UserData = siteUnit[112:
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
    siteNum = []
    siteVal = []
    # siteNumUser = []
    # siteValUser = []
    # for siteName in original:
    #     idx = df['Site No.'].tolist().index(siteName)
    #     siteNum.append(int(df['Site No.'].values[idx]))
    #     siteVal.append(df['Plume length[m]'].values[idx])
    # for siteName in UserData:
    #     idx = nf['Site No.'].tolist().index(siteName)
    #     siteNumUser.append(int(nf['Site No.'].values[idx]))
    #     siteValUser.append(nf['Plume length[m]'].values[idx])
    bar1 = go.Bar(
        x=df['Site No.'],
        y=df['Plume length[m]'],
        name='Original Data',
        marker=dict(
            color='#003f5c'
        )
    )
    bar2 = go.Bar(
        x=user_site_no,
        y=plume_length,
        name='User Data',
        marker=dict(
            color='#ffa600'
        )
    )
    bar3 = go.Bar(
        x=user_site_no_similar_data,
        y=similar_data,
        name='Similar Data',
        marker=dict(
            color='#FF6361'
        )
    )
    data = [bar1, bar2,bar3]

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
            title='<b>Site Number</b>',
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='<b>Plume Length</b>',
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


def create_boxplot(boxplot, table_data, index):
    original_data = df[boxplot].values.tolist()
    user_data = [item[index] for item in table_data]
    merged_list = original_data + user_data
    trace1 = go.Box(
        y=df[boxplot],
        name='Original database',
        boxmean=True,
        jitter=0.3,
        pointpos=1.5,
        marker = dict(
            color='red'
        )
    )
    trace2 = go.Box(
        y=merged_list,
        name='User and original database',
        boxmean=True,
        jitter=0.3,
        pointpos=1,
        marker=dict(
            color='blue'
        )
    )
    layout = go.Layout(
        title=boxplot,
        titlefont=dict(
            size=18,

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
            titlefont=dict(
                size=18
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)'
        )
    )
    if not user_data:
        data = [trace1]
    else:
        data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_histogram(histogramFeature, table_data, index, parameter):
    plume_data = df[parameter]
    if parameter == "Electron Donor[mg/l]":
        plume_data = [int(x) for x in plume_data]
    plume_data = [x for x in plume_data if str(x) != 'nan']

    mu, std = norm.fit(plume_data)
    x = np.linspace(0, max(plume_data))
    # Get current size
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 10  # width
    fig_size[1] = 5
    plt.rcParams["figure.figsize"] = fig_size
    plt.hist(plume_data, density=True, color='#ffa600', alpha=0.7)
    if histogramFeature == 'Gaussian':
        y_pdf = ss.norm.pdf(x, mu, std)
        plt.plot(x, y_pdf, color='#d45087', linewidth=3)
    elif histogramFeature == 'Log Normal':
        y_log = ss.lognorm.pdf(x, mu, std)
        plt.plot(x, y_log, color='#a05195', linewidth=3)
    else:
        y_expo = ss.expon.pdf(x, mu, std)
        plt.plot(x, y_expo, color='#665191', linewidth=3)
    plt.title(histogramFeature, fontsize=20, fontweight='bold')
    plt.xlabel(parameter, fontsize=18, fontweight='bold')
    plt.ylabel('Frequency', fontsize=18, fontweight='bold')
    fig = plt.gcf()
    data = tls.mpl_to_plotly(fig)
    fig = go.Figure(data=data)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
