import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as ply
import plotly.graph_objs as go

os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\modified')

# Read from file
print('Reading data...')
# data = pd.read_pickle(r'Balance_Demand.pkl')
data = pd.read_pickle(r'Balance_Demand_Mod.pkl')

cols = ['Demand (% of forecast)',
        'Forecast Error (MW)',
        'Demand (MW) (Adjusted)',
        'Demand Forecast (MW)',
        ]

bal_areas = sorted(list(set(data.loc[:, 'Balancing Authority'])))

data[data['Demand (MW) (Adjusted)'] == 0] = None
data[data['Demand Forecast (MW)'] == 0] = None
data['Demand (% of forecast)'] = data['Demand (MW) (Adjusted)'] / data['Demand Forecast (MW)']
data['Forecast Error (MW)'] = data['Demand Forecast (MW)'] - data['Demand (MW) (Adjusted)']

for ba in bal_areas:
    print(f'\nBeginning processing for {ba}...')
    data_sel = data.loc[data['Balancing Authority'] == ba, cols]

    # gt_total = data_sel.prod(axis=1, skipna=False)
    # disp_sel = gt_total[gt_total != 0].index

    print('Final data shaping...')
    layout = go.Layout(hovermode='closest',
                       yaxis=dict(
                           domain=[0, 0.45],
                           ),
                       yaxis2=dict(
                           domain=[0.55, 1.0],
                           hoverformat=',.1%',
                           tickformat=',.1%',
                           title='Demand (% of forecast)',
                           ),
                       yaxis3=dict(
                           overlaying='y2',
                           hoverformat=',d',
                           tickformat=',d',
                           side='right',
                           title='Forecast Error (MW)',
                           ),
                       )
    fig = go.Figure(layout=layout)

    fig.add_trace(go.Scatter(name='Demand (% of forecast)',
                             x=data_sel.index,
                             y=data_sel['Demand (% of forecast)'],
                             hoverinfo='text+x+y',
                             text='Demand (% of forecast)',
                             yaxis='y2'))
    fig.add_trace(go.Scatter(name='Forecast Error (MW)',
                             x=data_sel.index,
                             y=data_sel['Forecast Error (MW)'],
                             hoverinfo='text+x+y',
                             text='Forecast Error (MW)',
                             yaxis='y3'))
    fig.add_trace(go.Scatter(name='Demand (MW)',
                             x=data_sel.index,
                             y=data_sel['Demand (MW) (Adjusted)'],
                             hoverinfo='text+x+y',
                             text='Demand (MW)',
                             yaxis='y'))
    fig.add_trace(go.Scatter(name='Demand Forecast (MW)',
                             x=data_sel.index,
                             y=data_sel['Demand Forecast (MW)'],
                             hoverinfo='text+x+y',
                             text='Demand Forecast (MW)',
                             yaxis='y'))
    

    print('Creating plot...')
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\BA Charts by Type\Forecasting')
    ply.plot(fig, filename=f'{ba} EIA 930 Demand Forecast.html', auto_open=False)
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\Balancing Areas')
    try:
        os.mkdir(f'{ba}')
    except FileExistsError:
        pass
    ply.plot(fig, filename=f'{ba}\\{ba} EIA 930 Demand Forecast.html', auto_open=False)
    print('Plot created!')
