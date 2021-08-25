import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as ply
import plotly.graph_objs as go

os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\modified')

# Read from file
print('Reading data...')
data = pd.read_pickle(r'Interchange_Grouped.pkl')
source_BAs = sorted(list(set(data.loc[:, 'Balancing Authority'])))

for ba in source_BAs:
    print(f'\nBeginning processing for {ba}...')
    data_sel = data.loc[data['Balancing Authority'] == ba, :]

    print('Pivoting...')
    data_pivot = data_sel.pivot(columns='Directly Interconnected Balancing Authority', values='Interchange (MW)')
    data_pivot['Net Exports'] = data_pivot.sum(axis=1)

    print('Final data shaping...')
    chart_sel = [go.Scatter(name=col,
                            x=data_pivot.index,
                            y=data_pivot[col],
                            hoverinfo='text+x+y',
                            text=col)
                 for col in data_pivot]

    layout = go.Layout(hovermode='closest')
    fig_sel = go.Figure(data=chart_sel, layout=layout)

    print('Creating plot...')
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\BA Charts by Type\Interchange')
    ply.plot(fig_sel, filename=f'{ba} EIA 930 Interchange.html', auto_open=False)
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\Balancing Areas')
    try:
        os.mkdir(f'{ba}')
    except FileExistsError:
        pass
    ply.plot(fig_sel, filename=f'{ba}\\{ba} EIA 930 Interchange.html', auto_open=False)
    print('Plot created!')

