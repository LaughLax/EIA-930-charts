import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as ply
import plotly.graph_objs as go

os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\modified')

# Read from file
data_solar = pd.read_csv(r'EIA930_BALANCE_2018_Jul_Dec.csv',
                         usecols=['Balancing Authority',
                                  'UTC Time at End of Hour',
                                  'Net Generation (MW) from Solar'],
                         index_col=1,
                         infer_datetime_format=True,
                         low_memory=False,
                         na_filter=False,
                         parse_dates=True)
data_wind = pd.read_csv(r'EIA930_BALANCE_2018_Jul_Dec.csv',
                        usecols=['Balancing Authority',
                                 'UTC Time at End of Hour',
                                 'Net Generation (MW) from Wind'],
                        index_col=1,
                        infer_datetime_format=True,
                        low_memory=False,
                        na_filter=False,
                        parse_dates=True)

def my_conv(num_str):
    if num_str == '':
        return np.nan
    if ',' in num_str:
        num_str = num_str.replace(',','')
    return int(num_str)

# Convert to numeric
data_solar['Net Generation (MW) from Solar'] = pd.to_numeric(data_solar['Net Generation (MW) from Solar'].apply(my_conv))
data_wind['Net Generation (MW) from Wind'] = pd.to_numeric(data_wind['Net Generation (MW) from Wind'].apply(my_conv))

# Pivot
data_solar = data_solar.pivot(columns='Balancing Authority',
                              values='Net Generation (MW) from Solar')
data_wind = data_wind.pivot(columns='Balancing Authority',
                            values='Net Generation (MW) from Wind')

# Add a Total column
# data_solar['Total'] = data_solar.sum(axis=1)
# data_wind['Total'] = data_wind.sum(axis=1)

ba_total_solar = data_solar.sum(axis=0)
disp_solar = ba_total_solar[ba_total_solar > 0].index
ba_total_wind = data_wind.sum(axis=0)
disp_wind = ba_total_wind[ba_total_wind > 0].index

os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out')

chart_solar = [go.Scatter(name=col,
                          x=data_solar.index,
                          y=data_solar[col],
                          hoverinfo='text+x+y',
                          text=col)
               for col in disp_solar]

chart_wind = [go.Scatter(name=col,
                         x=data_wind.index,
                         y=data_wind[col],
                         hoverinfo='text+x+y',
                         text=col)
              for col in disp_wind]

layout = go.Layout(
    hovermode='closest')

fig_solar = go.Figure(data=chart_solar, layout=layout)
fig_wind = go.Figure(data=chart_wind, layout=layout)

ply.plot(fig_solar, filename='solar.html')
ply.plot(fig_wind, filename='wind.html')
