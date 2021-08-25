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

other_cols = ['Demand (MW) (Adjusted)',
              'Net Generation (MW) (Adjusted)',
              ]

bal_areas = sorted(list(set(data.loc[:, 'Balancing Authority'])))

for ba in bal_areas:
# for ba in ['CISO']:
    print(f'\nBeginning processing for {ba}...')
    data_sel = data.loc[data['Balancing Authority'] == ba, other_cols]

    gt_total = data_sel.sum(axis=0)
    disp_sel = gt_total[gt_total != 0].index

    print('Shaping data for chart...')
    chart_sel = [dict(name=col,
                      x=data_sel.index,
                      y=data_sel[col],
                      hoverinfo='text+x+y',
                      text=col)
                 for col in disp_sel]

    layout = go.Layout(hovermode='closest')
    fig_sel = go.Figure(data=chart_sel, layout=layout)

    print('Creating plot...')
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\BA Charts by Type\Demand')
    ply.plot(fig_sel, filename=f'{ba} EIA 930 Demand.html', auto_open=False)
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\Balancing Areas')
    try:
        os.mkdir(f'{ba}')
    except FileExistsError:
        pass
    ply.plot(fig_sel, filename=f'{ba}\\{ba} EIA 930 Demand.html', auto_open=False)
    print('Plot created!')

    # Ramp data
    print(f'Processing ramp data...')
    data_sel['Ramp'] = data_sel['Demand (MW) (Adjusted)'].diff()

    print('Final data shaping...')
    chart_sel = dict(name='Ramp (MW)',
                     x=data_sel.index,
                     y=data_sel['Ramp'],
                     hoverinfo='text+x+y',
                     text='Ramp (MW)')

    layout = go.Layout(hovermode='closest')
    fig_sel = go.Figure(data=chart_sel, layout=layout)

    print('Creating plot...')
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\BA Charts by Type\Demand Ramp')
    ply.plot(fig_sel, filename=f'{ba} EIA 930 Demand Ramp.html', auto_open=False)
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\Balancing Areas')
    try:
        os.mkdir(f'{ba}')
    except FileExistsError:
        pass
    ply.plot(fig_sel, filename=f'{ba}\\{ba} EIA 930 Demand Ramp.html', auto_open=False)
    print('Plot created!')
