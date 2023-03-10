import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import getParser
import getParameter

def getCostOfSales(file_dir, country_code, last_date):
    
    print(f' [INFO] [COS]: Generating COS report - {getParser.getOpeningTBFile(file_dir, country_code)}')

    report_type = 'Quarter' #'Month No'
    df_sf_report = pd.read_csv(getParser.getSFChronoSegmentFile(file_dir, country_code), encoding = 'latin1')
    df_sf_report['Date'] =  pd.to_datetime(df_sf_report['Date'])
    #df_sf_report['Close Date'] =  pd.to_datetime(df_sf_report['Close Date'])
    df_sf_report['Invoice Date'] =  pd.to_datetime(df_sf_report['Invoice Date'])
    df_sf_report['Revenue_Quarter'] = df_sf_report.groupby(['Account Name: Region', report_type])['Net Revenue'].transform('sum')
    # print(df_sf_report['Date'].count())
    df_sf_report.head()


    list_country = ['MY', 'SGP', 'PH', 'IN']
    currency_all = getParameter.currency_all
    frames = []
    for country in list_country:
        currency = currency_all[country]
        #print(currency)
        df_gl = pd.read_csv(getParser.getMasterFile(file_dir, country), encoding = 'latin1')
        df_gl.insert(len(df_gl.axes[1]), 'Country', country, True)
        df_gl.insert(len(df_gl.axes[1]), 'Currency', currency, True)
        frames.append(df_gl)
        
    df_gl_sgp = pd.concat(frames)
    # print(df_gl_sgp.columns)
    # df_gl_sgp.reset_index(drop=True, inplace=True)
    df_gl_sgp['Currency'] = df_gl_sgp['Currency'].astype(float)
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

    #df_gl_sgp['Amount'] = df_gl_sgp.groupby(['Salesforce', 'Month No'])['Opening_Debit'].transform('sum')
    #df_gl_sgp['Amount'] = df_gl_sgp.groupby(['Salesforce', 'Month No']).apply(lambda x: x['Opening_Debit'].sum() - x['Opening_Credit'].sum())

    # df_gl_sgp['Debit_Amount'] = df_gl_sgp.groupby(['Salesforce', 'Month No'])['Opening_Debit'].transform('sum')
    # df_gl_sgp['Credit_Amount'] = df_gl_sgp.groupby(['Salesforce', 'Month No'])['Opening_Credit'].transform('sum')
    # df_gl_sgp['Amount'] = df_gl_sgp['Credit_Amount'] - df_gl_sgp['Debit_Amount']
    # df_gl_sgp['Cost_Of_Sales'] = np.where(df_gl_sgp['Amount'] < 0, df_gl_sgp['Amount'], 0)



    df_gl_sgp['Debit_Amount'] = df_gl_sgp.groupby(['Salesforce', report_type])['Opening_Debit'].transform('sum')
    df_gl_sgp['Credit_Amount'] = df_gl_sgp.groupby(['Salesforce', report_type])['Opening_Credit'].transform('sum')
    # check the datatype
    # print(df_gl_sgp['Credit_Amount'].dtypes)
    # print(df_gl_sgp['Debit_Amount'].dtypes)
    # print(df_gl_sgp['Currency'].dtypes)
    df_gl_sgp['Amount'] = (df_gl_sgp['Credit_Amount'] - df_gl_sgp['Debit_Amount']) / df_gl_sgp['Currency']
    df_gl_sgp['Cost_Of_Sales'] = np.where(df_gl_sgp['Amount'] < 0, df_gl_sgp['Amount'], 0)
    # print(df_gl_sgp['Date'].count())

    # Merge sf report with gl report
    df_sf_report_ = df_sf_report[['Account Name: Account Name', 'Account Name: Region', report_type]].copy()
    df_sf_report_.drop_duplicates(subset=['Account Name: Account Name', report_type], keep='first', inplace=True)
    df_cos_without_revenue = pd.merge(df_gl_sgp, df_sf_report_, how='left', \
                            left_on=['Salesforce', report_type], right_on=['Account Name: Account Name', report_type])
    #print(df_cos_without_revenue.columns)
    df_cos_without_revenue.rename(columns = {'Account Name: Account Name':'COS_Without_Revenue'}, inplace = True)
    #print(df_cos_without_revenue.columns)
    df_cos_without_revenue['COS_Without_Revenue'] = df_cos_without_revenue['COS_Without_Revenue'].fillna('Not Available')
    df_cos_without_revenue.to_csv(getParser.getCOSWithoutRevenueFile(file_dir, country_code), mode='w', sep=',', encoding='utf-8', index=False)
    # print(df_cos_without_revenue['Date'].count())



    # Merge sf report with gl report
    df_gl_sgp.drop_duplicates(subset=['Salesforce', report_type], keep='first', inplace=True)
    df_final_data = pd.merge(df_sf_report, df_gl_sgp, how='left', \
                            left_on=['Account Name: Account Name', report_type], right_on=['Salesforce', report_type])


    # Process France Data
    df_gl_sgp = pd.read_csv(getParser.getMasterFile(file_dir, country_code='FR'), encoding = 'latin1')

    country = 'FR'
    currency = currency_all['FR']
    df_gl_sgp.insert(len(df_gl_sgp.axes[1]), 'Country', country, True)
    df_gl_sgp.insert(len(df_gl_sgp.axes[1]), 'Currency', currency, True)
    df_gl_sgp['Currency'] = df_gl_sgp['Currency'].astype(float)
        

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

    df_gl_sgp['Debit_Amount'] = df_gl_sgp.groupby(['Grouping_1', report_type])['Opening_Debit'].transform('sum')
    df_gl_sgp['Credit_Amount'] = df_gl_sgp.groupby(['Grouping_1', report_type])['Opening_Credit'].transform('sum')
    df_gl_sgp['Amount'] = (df_gl_sgp['Credit_Amount'] - df_gl_sgp['Debit_Amount']) / df_gl_sgp['Currency']
    df_gl_sgp['Cost_Of_Sales_Quarter'] = np.where(df_gl_sgp['Amount'] < 0, df_gl_sgp['Amount'], 0)
    df_gl_sgp.insert(len(df_gl_sgp.axes[1]), 'Account Name: Region', 'Europe', True)
    # print(df_gl_sgp['Date'].count())

    df_gl_sgp.drop_duplicates(subset=['Account Name: Region', report_type], keep='first', inplace=True)
    df_final_data_ = pd.merge(df_final_data, df_gl_sgp[['Account Name: Region', 'Cost_Of_Sales_Quarter', report_type]],\
                            how='left', left_on=['Account Name: Region', report_type], \
                            right_on=['Account Name: Region', report_type])        

    df_final_data_filtered = df_final_data_[df_final_data_['Account Name: Region'].str.contains('Europe', case=False, na=False)]
    for row_index, row in df_final_data_filtered.iterrows():
        df_final_data_.loc[row_index, 'Cost_Of_Sales'] = (row['Net Revenue'] / row['Revenue_Quarter']) * row['Cost_Of_Sales_Quarter']

    df_final_data_['Gross_Margin'] = df_final_data_['Gross Revenue'] - abs(df_final_data_['Cost_Of_Sales'])
    #df_final_data_ = df_final_data_.replace(r'\n',' ', regex=True) 
    df_final_data_.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
    df_final_data_.to_csv(getParser.getSFCOSFile(file_dir, country_code, report_type), mode='w', sep=',', encoding='utf-8', index=False)
    # print(df_final_data_['Date_x'].count())
    

    # cost greater than revenue
    df_cost_greater_than_revenue = df_final_data_[df_final_data_['Gross_Margin'] < 0]
    df_cost_greater_than_revenue.to_csv(getParser.getCOSGreaterThanRevenueFile(file_dir, country_code), mode='w', sep=',', encoding='utf-8', index=False)


    df_final_data_.head()
