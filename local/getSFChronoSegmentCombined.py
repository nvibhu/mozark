import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import getParser

def getSFChronoSegmentCombined(file_dir, country_code, last_date):
    
    df_sf_complete_report = pd.read_csv(getParser.getSFChronoFile(file_dir, country_code), encoding = 'latin1')
    df_sf_complete_report['Date'] =  pd.to_datetime(df_sf_complete_report['Date'])
    df_sf_complete_report.head()
    print(df_sf_complete_report['Date'].count())

    df_sf_segment_report = pd.read_csv(getParser.getSFSegmentFile(file_dir, country_code), encoding = 'latin1')
    df_sf_segment_report.head()

    # Merge complete report with segment report
    df_sf_segment_report.drop_duplicates(subset=['Account Name'], keep='first', inplace=True)
    df_sf_merged = pd.merge(df_sf_complete_report, df_sf_segment_report, how='left', \
                            left_on=['Account Name: Account Name'], right_on=['Account Name'])
    df_sf_merged.rename(columns = {'Month_rate (converted)':'Gross Revenue'}, inplace = True)
    df_sf_merged['PassThrough'] = df_sf_merged['PassThrough'].astype(float)
    df_sf_merged['PassThrough'] = df_sf_merged['PassThrough'].fillna(0)
    df_sf_merged['Count'] = df_sf_merged.groupby(['Chrono Name'])['Chrono Name'].transform('count')
    df_sf_merged['Invoice'] = df_sf_merged['Invoiced Revenue (converted)'] / df_sf_merged['Count']
    df_sf_merged['Invoice'] = df_sf_merged['Invoice'].astype(float)
    df_sf_merged['Invoice'] = df_sf_merged['Invoice'].fillna(0)
    df_sf_merged['Final Order'] = df_sf_merged['Project Revenue (converted)'] / df_sf_merged['Count']
    df_sf_merged['Recurring'] = df_sf_merged['ACTIVITY'].apply(lambda x: 'One-Time' if x == 'One-Time' else 'Recurring')
    df_sf_merged['Net Revenue'] = df_sf_merged['Gross Revenue'] * ((100 - df_sf_merged['PassThrough']) / 100)
    df_sf_merged['Unbilled'] = df_sf_merged['Gross Revenue'] - df_sf_merged['Invoice']
    #df_sf_merged.loc[df_sf_merged['Recurring'] == 'Recurring', 'Status'] = 'Found' 
    df_sf_merged['Recurring Rev'] = np.where(df_sf_merged['Recurring'] == 'Recurring', df_sf_merged['Net Revenue'], 0)
    df_sf_merged['Month No'] = df_sf_merged['Date'].dt.month
    # df_sf_merged['Quarter'] = np.where(df_sf_merged['Month No'].isin([10,11,12]), 'Q3', \
    #                                   (df_sf_merged['Month No'].isin([7,8,9]), 'Q2', \
    #                                   (df_sf_merged['Month No'].isin([4,5,6]), 'Q1', 'Q4')))

    # create a list of our conditions based on month no
    quarter_conditions = [
        (df_sf_merged['Month No'].isin([10,11,12])),
        (df_sf_merged['Month No'].isin([7,8,9])),
        (df_sf_merged['Month No'].isin([4,5,6])),
        (df_sf_merged['Month No'].isin([1,2,3]))
        ]
    # create a list of the values we want to assign for each condition
    quarter_values = ['Q3', 'Q2', 'Q1', 'Q4']

    # create a new column and use np.select to assign values to it using our lists as arguments
    df_sf_merged['Quarter'] = np.select(quarter_conditions, quarter_values)
    df_sf_merged.to_csv(getParser.getSFChronoSegmentFile(file_dir, country_code), mode='w', sep=',', encoding='latin1', index=False)
    print(df_sf_merged['Date'].count())
    df_sf_merged.head()