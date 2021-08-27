import os
import pandas as pd
import plotly.offline as ply
import plotly.graph_objs as go

# Read from file
print('Reading data...')
data = pd.read_pickle(r'modified\Balance_Grouped.pkl')
# data = pd.read_pickle(r'modified\Balance_Grouped_Mod.pkl')

gentypes = ['Nuclear',
            'Coal',
            'All Petroleum Products',
            'Hydropower and Pumped Storage',
            'Natural Gas',
            'Other Fuel Sources',
            'Wind',
            'Solar',
            'Unknown Fuel Sources']
gencols = [f'Net Generation (MW) from {gen}' for gen in gentypes]

bal_areas = sorted(list(set(data.loc[:, 'Balancing Authority'])))

if not os.path.exists(r'out\BA Charts by Type\Generation Mix'):
    os.makedirs(r'out\BA Charts by Type\Generation Mix')

for ba in bal_areas:
    print(f'\nBeginning processing for {ba}...')
    data_sel = data.loc[data['Balancing Authority'] == ba, gencols].sort_index()

    gentype_total = data_sel.sum(axis=0)
    disp_sel = gentype_total[gentype_total != 0].index

    print('Final data shaping...')
    chart_sel = [dict(name=col,
                      x=data_sel.index,
                      y=data_sel[col],
                      hoverinfo='text+x+y',
                      text=col,
                      stackgroup='one',
                      mode='lines',
                      hoveron='points+fills')
                 for col in disp_sel]

    layout = go.Layout()# hovermode='closest')
    fig_sel = go.Figure(data=chart_sel, layout=layout)

    print('Creating plot...')

    if not os.path.exists(f'out\\Balancing Areas\\{ba}'):
        os.makedirs(f'out\\Balancing Areas\\{ba}')
    ply.plot(fig_sel, filename=f'out\\Balancing Areas\\{ba}\\{ba} EIA 930 Generation Sources.html', auto_open=False)
    ply.plot(fig_sel, filename=f'out\\BA Charts by Type\\Generation Mix\\{ba} EIA 930 Generation Sources.html', auto_open=False)
    print('Plot created!')

    print('Final data shaping...')
    tot = data_sel.sum(axis=1)
    chart_sel = [dict(name=col,
                      x=data_sel.index,
                      y=data_sel[col] / tot,
                      hoverinfo='text+x+y',
                      text=col,
                      stackgroup='one',
                      mode='lines',
                      hoveron='points+fills')
                 for col in disp_sel]

    layout = go.Layout(hovermode='x',
                       yaxis=dict(
                            hoverformat=',.1%',
                            tickformat=',.1%')
                       )
    fig_sel = go.Figure(data=chart_sel, layout=layout)

    print('Creating plot...')
    ply.plot(fig_sel, filename=f'out\\BA Charts by Type\\Generation Mix\\{ba} EIA 930 Generation Sources (Percent).html', auto_open=False)
    ply.plot(fig_sel, filename=f'out\Balancing Areas\\{ba}\\{ba} EIA 930 Generation Sources (Percent).html', auto_open=False)
    print('Plot created!')

if not os.path.exists(r'out\Fuel Sources'):
    os.makedirs(r'out\Fuel Sources')

for gentype in gentypes:
    print(f'\nBeginning processing for {gentype}...')
    gen_str = f'Net Generation (MW) from {gentype}'
    
    data_sel = data.loc[:, ['Balancing Authority',
                            gen_str]]

    # Pivot
    print('Pivoting...')
    data_sel = data_sel.pivot(columns='Balancing Authority',
                              values=gen_str)

    # Add a Total column
    # data_sel['Total'] = data_sel.sum(axis=1)

    ba_total = data_sel.sum(axis=0)
    disp_sel = ba_total[ba_total > 0].index

    print('Final data shaping...')
    chart_sel = [go.Scatter(name=col,
                            x=data_sel.index,
                            y=data_sel[col],
                            hoverinfo='text+x+y',
                            text=col)
                 for col in disp_sel]

    layout = go.Layout(hovermode='closest')
    fig_sel = go.Figure(data=chart_sel, layout=layout)

    print('Creating plot...')
    ply.plot(fig_sel, filename=f'out\\Fuel Sources\\{gentype}.html', auto_open=False)
    print('Plot created!')
