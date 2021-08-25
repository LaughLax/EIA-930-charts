import os
from multiprocessing import Pool
import numpy as np
import pandas as pd

NUM_PROCESSES = 6

num_cols = {'Demand Forecast (MW)',
            'Demand (MW)',
            'Net Generation (MW)',
            'Demand (MW) (Adjusted)',
            'Net Generation (MW) (Adjusted)',
            'Interchange (MW)',
            }
gentypes = ['Nuclear',
            'Coal',
            'All Petroleum Products',
            'Hydropower and Pumped Storage',
            'Natural Gas',
            'Other Fuel Sources',
            'Wind',
            'Solar',
            'Unknown Fuel Sources',
            ]
num_cols |= set(f'Net Generation (MW) from {gen}' for gen in gentypes)

non_wecc_areas = ['AEC', 'AECI', 'CPLE', 'CPLW', 'DEAA',
                  'DUK', 'EEI', 'ERCO', 'FMPP', 'FPC',
                  'FPL', 'GVL', 'HST', 'ISNE', 'JEA',
                  'LGEE', 'MISO', 'NSB', 'NYIS', 'OVEC',
                  'PJM', 'PSEI', 'SC', 'SCEG', 'SEC',
                  'SEPA', 'SOCO', 'SPA', 'SWPP', 'TAL',
                  'TEC', 'TVA', 'YAD',]


def my_conv(num_str):
    if isinstance(num_str, int) or isinstance(num_str, float):
        return num_str
    if num_str == '':
        return np.nan
    if ',' in num_str:
        num_str = num_str.replace(',','')
    return int(num_str)

def read_file(filename):
    print(f'Reading {filename}')
    if os.path.splitext(filename)[-1] == '.csv':
        df = pd.read_csv(filename,
                         index_col='UTC Time at End of Hour',
                         # usecols = ['ColName1', 'ColName2', 'ColName3'], # only in interx
                         infer_datetime_format=True,
                         low_memory=False,
                         na_filter=False,
                         parse_dates=True)
    else:
        df = pd.read_excel(filename,
                           index_col=4,
                           na_filter=False,
                           parse_dates=True)
    
    # for ba in non_wecc_areas:
    #     df = df[df['Balancing Authority'] != ba]
    # df = df[~df['Balancing Authority'].isin(non_wecc_areas)]
    cols_to_num = set(df.columns) & num_cols
    df.loc[:, cols_to_num] = df.loc[:, cols_to_num].applymap(my_conv)

    return df

def read_fileset(filenames):
    with Pool(NUM_PROCESSES) as p:
        dfs = p.map(read_file, filenames)    

    print('Combining data...')
    df_master = dfs[0]
    for i in range(1, len(dfs)):
        df_master = df_master.append(dfs[i])

    return df_master

if __name__ == '__main__':
    bal_raw = [# r'raw\EIA930_BALANCE_2021_Jul_Dec.csv',
               r'raw\EIA930_BALANCE_2021_Jan_Jun.csv',
               r'raw\EIA930_BALANCE_2020_Jul_Dec.csv',
               r'raw\EIA930_BALANCE_2020_Jan_Jun.csv',
               r'raw\EIA930_BALANCE_2019_Jul_Dec.csv',
               r'raw\EIA930_BALANCE_2019_Jan_Jun.csv',
               r'raw\EIA930_BALANCE_2018_Jul_Dec.csv',
               r'raw\EIA930_BALANCE_2018_Jan_Jun.csv',
               r'raw\EIA930_BALANCE_2017_Jul_Dec.csv',
               r'raw\EIA930_BALANCE_2017_Jan_Jun.csv',
               r'raw\EIA930_BALANCE_2016_Jul_Dec.csv',
               r'raw\EIA930_BALANCE_2016_Jan_Jun.csv',
               r'raw\EIA930_BALANCE_2015_Jul_Dec.csv',
               ]

    bal_mod = [# r'modified\EIA930_BALANCE_2021_Jul_Dec.xlsx',
               r'modified\EIA930_BALANCE_2021_Jan_Jun.xlsx',
               r'modified\EIA930_BALANCE_2020_Jul_Dec.xlsx',
               r'modified\EIA930_BALANCE_2020_Jan_Jun.xlsx',
               r'modified\EIA930_BALANCE_2019_Jul_Dec.xlsx',
               r'modified\EIA930_BALANCE_2019_Jan_Jun.xlsx',
               r'modified\EIA930_BALANCE_2018_Jul_Dec.xlsx',
               r'modified\EIA930_BALANCE_2018_Jan_Jun.xlsx',
               r'modified\EIA930_BALANCE_2017_Jul_Dec.xlsx',
               r'modified\EIA930_BALANCE_2017_Jan_Jun.xlsx',
               r'modified\EIA930_BALANCE_2016_Jul_Dec.xlsx',
               r'modified\EIA930_BALANCE_2016_Jan_Jun.xlsx',
               r'modified\EIA930_BALANCE_2015_Jul_Dec.xlsx',
               ]
    
    bal_recent = [# r'raw\EIA930_BALANCE_2021_Jul_Dec.csv',
                  r'raw\EIA930_BALANCE_2021_Jan_Jun.csv',
                  r'raw\EIA930_BALANCE_2020_Jul_Dec.csv',
                  r'raw\EIA930_BALANCE_2020_Jan_Jun.csv',
                  r'raw\EIA930_BALANCE_2019_Jul_Dec.csv',
                  r'raw\EIA930_BALANCE_2019_Jan_Jun.csv',
                  r'raw\EIA930_BALANCE_2018_Jul_Dec.csv',
                  ]
    
    bal_recent_mod = [# r'modified\EIA930_BALANCE_2021_Jul_Dec.xlsx',
                      r'modified\EIA930_BALANCE_2021_Jan_Jun.xlsx',
                      r'modified\EIA930_BALANCE_2020_Jul_Dec.xlsx',
                      r'modified\EIA930_BALANCE_2020_Jan_Jun.xlsx',
                      r'modified\EIA930_BALANCE_2019_Jul_Dec.xlsx',
                      r'modified\EIA930_BALANCE_2019_Jan_Jun.xlsx',
                      r'modified\EIA930_BALANCE_2018_Jul_Dec.xlsx',
                      ]
    
    interx = [# r'raw\EIA930_INTERCHANGE_2021_Jul_Dec.csv',
              r'raw\EIA930_INTERCHANGE_2021_Jan_Jun.csv',
              r'raw\EIA930_INTERCHANGE_2020_Jul_Dec.csv',
              r'raw\EIA930_INTERCHANGE_2020_Jan_Jun.csv',
              r'raw\EIA930_INTERCHANGE_2019_Jul_Dec.csv',
              r'raw\EIA930_INTERCHANGE_2019_Jan_Jun.csv',
              r'raw\EIA930_INTERCHANGE_2018_Jul_Dec.csv',
              r'raw\EIA930_INTERCHANGE_2018_Jan_Jun.csv',
              r'raw\EIA930_INTERCHANGE_2017_Jul_Dec.csv',
              r'raw\EIA930_INTERCHANGE_2017_Jan_Jun.csv',
              r'raw\EIA930_INTERCHANGE_2016_Jul_Dec.csv',
              r'raw\EIA930_INTERCHANGE_2016_Jan_Jun.csv',
              ]

    subreg = [# r'raw\EIA930_SUBREGION_2021_Jul_Dec.csv',
              r'raw\EIA930_SUBREGION_2021_Jan_Jun.csv',
              r'raw\EIA930_SUBREGION_2020_Jul_Dec.csv',
              r'raw\EIA930_SUBREGION_2020_Jan_Jun.csv',
              r'raw\EIA930_SUBREGION_2019_Jul_Dec.csv',
              r'raw\EIA930_SUBREGION_2019_Jan_Jun.csv',
              r'raw\EIA930_SUBREGION_2018_Jul_Dec.csv',
              ]        

    print('BALANCE (all, raw)')
    print('Reading files...')
    df = read_fileset(bal_raw)
    print('Writing to file...')
    df.to_pickle(r'modified\Balance_Demand.pkl')
    print('Done!\n')
    
    print('BALANCE (all, modified)')
    print('Reading files...')
    df = read_fileset(bal_mod)
    print('Writing to file...')
    df.to_pickle(r'modified\Balance_Demand_Mod.pkl')
    print('Done!\n')
    
    print('BALANCE (recent, raw)')
    print('Reading files...')
    df = read_fileset(bal_recent)
    print('Writing to file...')
    df.to_pickle(r'modified\Balance_Grouped.pkl')
    print('Done!\n')
    
    print('BALANCE (recent, modified)')
    print('Reading files...')
    df = read_fileset(bal_recent_mod)
    print('Writing to file...')
    df.to_pickle(r'modified\Balance_Grouped_Mod.pkl')
    print('Done!\n')
    
    print('INTERCHANGE (raw)')
    print('Reading files...')
    df = read_fileset(interx)
    print('Writing to file...')
    df.to_pickle(r'modified\Interchange_Grouped.pkl')
    print('Done!\n')

    print('SUBREGION (raw)')
    print('Reading files...')
    df = read_fileset(subreg)
    df.loc[:, ['Balancing Authority']] = df['Balancing Authority'].astype(str) + '-' + df['Sub-Region'].astype(str)
    df.drop(columns='Sub-Region')
    print('Writing to file...')
    df.to_pickle(r'modified\Subregion_Grouped.pkl')
    print('Done!\n')
    
