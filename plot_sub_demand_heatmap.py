import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

DPI = 96
mpl.rcParams['figure.figsize'] = 1920 / DPI, 1080 / DPI
mpl.rcParams['savefig.dpi'] = DPI

os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\modified')

# Read from file
print('Reading data...')
data = pd.read_pickle(r'Subregion_Grouped.pkl')
# data = pd.read_pickle(r'Subregion_Demand_Mod.pkl')
data.loc[data['Demand (MW)'] == 0, 'Demand (MW)'] = np.nan
data.index = data.index - pd.Timedelta(hours=8)
# data = data.resample(rule='H').asfreq(fill_value=np.nan)

data['Week_no'] = data.index.to_period('W-SUN') # (data.index - data.index[0]).days // 7
data['Weekday'] = data.index.weekday
data['Hour'] = data.index.hour

data['Weekday-Hour'] = data['Weekday'] * 24 + data['Hour']

other_cols = ['Demand (MW)']

bal_areas = sorted(list(set(data['Balancing Authority'])))



# Demand  and Ramp Heatmaps
for ba in bal_areas:
# for ba in ['PACE']:
    print(f'\nBeginning processing for {ba}...')
    data_sel = data.loc[data['Balancing Authority'] == ba, ['Week_no', 'Weekday', 'Weekday-Hour', 'Demand (MW)']]
    if data_sel['Demand (MW)'].sum() == 0:
        continue
    print(f'Processing demand data...')

    month_1 = set(np.flatnonzero(data_sel.index.month == 1))
    day_1 = set(np.flatnonzero(data_sel.index.day == 1))
    hour_0 = set(np.flatnonzero(data_sel.index.hour == 0))
    ny = sorted(list(month_1 & day_1 & hour_0))
    weeks = [data_sel.iloc[hr]['Week_no'] for hr in ny]
    days = [data_sel.iloc[hr]['Weekday'] for hr in ny]    

    data_pivot = data_sel.pivot(index='Week_no', columns='Weekday-Hour', values='Demand (MW)')
    data_show = data_pivot.to_numpy().T

    plt.clf()
    img = plt.imshow(data_show,
                     # norm=mpl.colors.LogNorm(),
                     interpolation=None,
                     extent=[0, data_show.shape[1], data_show.shape[0], 0],
                     origin='upper',
                     aspect='auto',
                     cmap='jet')
    cbar = plt.colorbar()

    ax = plt.gca()
    ax.set_yticks([11, 35, 59, 83, 107, 131, 155])
    ax.set_yticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    [ax.axhline(y=y, color='black') for y in [24, 48, 72, 96, 120, 144]] # Draw lines to divide days

    week_no = np.flatnonzero([ind in weeks for ind in data_pivot.index]) # Identify which weeks include a year change
    for i, wk in enumerate(week_no):
        plt.plot([wk, wk, wk+1, wk+1], [7*24, days[i]*24, days[i]*24, 0], 'k') # Draw lines to divide years
    ax.set_xticks([wk - 26 for wk in week_no]) # Place tick marks for years
    ax.set_xticklabels([data_sel.index[0].year+i for i,e in enumerate(week_no)]) # Label tick marks for years
    
    plt.tight_layout()

    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\BA Charts by Type\Demand Heatmaps')
    plt.savefig(f'{ba} EIA 930 Demand Heatmap')
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\Balancing Areas')
    try:
        os.mkdir(f'{ba}')
    except FileExistsError:
        pass
    plt.savefig(f'{ba}\\{ba} EIA 930 Demand Heatmap')
    # plt.show()

    # Begin ramp heatmapping
    print(f'Processing ramp data...')
    data_sel['Ramp'] = data_sel['Demand (MW)'].diff()
    data_pivot = data_sel.pivot(index='Week_no', columns='Weekday-Hour', values='Ramp')
    data_show = data_pivot.to_numpy().T

    plt.clf()
    img = plt.imshow(data_show,
                     norm=mpl.colors.TwoSlopeNorm(vcenter=0),  # DivergingNorm renamed to TwoSlopeNorm in later matplotlib version
                     interpolation=None,
                     extent=[0, data_show.shape[1], data_show.shape[0], 0],
                     origin='upper',
                     aspect='auto',
                     cmap='RdBu_r')
    cbar = plt.colorbar()

    ax = plt.gca()
    ax.set_yticks([11, 35, 59, 83, 107, 131, 155])
    ax.set_yticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    [ax.axhline(y=y, color='black') for y in [24, 48, 72, 96, 120, 144]] # Draw lines to divide days

    week_no = np.flatnonzero([ind in weeks for ind in data_pivot.index]) # Identify which weeks include a year change
    for i, wk in enumerate(week_no):
        plt.plot([wk, wk, wk+1, wk+1], [7*24, days[i]*24, days[i]*24, 0], 'k') # Draw lines to divide years
    ax.set_xticks([wk - 26 for wk in week_no]) # Place tick marks for years
    ax.set_xticklabels([data_sel.index[0].year+i for i,e in enumerate(week_no)]) # Label tick marks for years
    
    plt.tight_layout()

    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\BA Charts by Type\Demand Ramp Heatmaps')
    plt.savefig(f'{ba} EIA 930 Demand Ramp Heatmap')
    os.chdir(r'C:\Users\dharalson\Desktop\local working folder\Misc\EIA 930\out\Balancing Areas')
    try:
        os.mkdir(f'{ba}')
    except FileExistsError:
        pass
    plt.savefig(f'{ba}\\{ba} EIA 930 Demand Ramp Heatmap')
    # plt.show()
