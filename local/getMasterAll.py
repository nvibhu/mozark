import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import getParser

def getMasterAll(file_dir):
    print(f' [INFO] [Master_All]: Getting files from dir - {file_dir}/Master/')

    list_country = ['MY', 'SGP', 'PH', 'IN', 'FR']
    currency_all = {
        'MY': 4.2,
        'SGP': 1.35,
        'PH': 51.6,
        'IN': 78,
        'FR': 0.9
    }
    frames = []
    for country in list_country:
        df_gl = pd.read_csv(getParser.getMasterFile(file_dir, country), encoding = 'latin1')
        currency = currency_all[country]
        df_gl.insert(len(df_gl.axes[1]), 'Country', country, True)
        df_gl.insert(len(df_gl.axes[1]), 'Currency', currency, True)
        frames.append(df_gl)
        
    df_gl_sgp = pd.concat(frames)
    df_gl_sgp['Date'] =  pd.to_datetime(df_gl_sgp['Date'])
    df_gl_sgp['Month No'] = df_gl_sgp['Date'].dt.month
    # create a list of our conditions based on month no
    quarter_conditions = [
        (df_gl_sgp['Month No'].isin([10,11,12])),
        (df_gl_sgp['Month No'].isin([7,8,9])),
        (df_gl_sgp['Month No'].isin([4,5,6])),
        (df_gl_sgp['Month No'].isin([1,2,3]))
        ]
    # create a list of the values we want to assign for each condition
    quarter_values = ['Q3', 'Q2', 'Q1', 'Q4']

    # create a new column and use np.select to assign values to it using our lists as arguments
    df_gl_sgp['Quarter'] = np.select(quarter_conditions, quarter_values)

    df_gl_sgp['Opening_Debit'] = df_gl_sgp['Opening_Debit'] / df_gl_sgp['Currency']
    df_gl_sgp['Opening_Credit'] = df_gl_sgp['Opening_Credit'] / df_gl_sgp['Currency']
    # Export combined data
    df_gl_sgp.to_csv(getParser.getMasterFileAll(file_dir, country_code='All'), mode='w', sep=',', encoding='latin1', index=False)



    df_gl_sgp['Debit_Amount'] = df_gl_sgp.groupby(['Country', 'Grouping'])['Opening_Debit'].transform('sum')
    df_gl_sgp['Credit_Amount'] = df_gl_sgp.groupby(['Country', 'Grouping'])['Opening_Credit'].transform('sum')
    df_gl_sgp['Amount'] = df_gl_sgp['Credit_Amount'] - df_gl_sgp['Debit_Amount']
    df_gl_sgp['Cost_Of_Sales'] = np.where(df_gl_sgp['Amount'] < 0, df_gl_sgp['Amount'], 0)

    df_gl_sgp['Amount_By_Month'] = df_gl_sgp.groupby(['Country', 'Grouping', 'Month No'])['Amount'].transform('sum')
    df_gl_sgp['Amount_By_Quarter'] = df_gl_sgp.groupby(['Country', 'Grouping', 'Quarter'])['Amount'].transform('sum')
    # Export combined data report
    df_gl_sgp.to_csv(getParser.getGroupWiseExpenseReport(file_dir, country_code='All'), mode='w', sep=',', encoding='latin1', index=False)

