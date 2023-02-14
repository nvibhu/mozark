import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import getParser

def getMasterIN(file_dir, country_code, last_date):

    print(f' [INFO] [{country_code}]: Getting files from dir - {getParser.getOpeningTBFile(file_dir, country_code)}')

    df_opening_balance = pd.read_csv(getParser.getOpeningTBFile(file_dir, country_code), encoding = 'latin1')
    #df_opening_balance['Date'] =  pd.to_datetime(df_opening_balance['Date']) #format='%d%b%Y:%H:%M:%S.%f'
    #df_opening_balance['Date'] =  pd.to_datetime(df_opening_balance['Date'], format='%d/%m/%y')
    df_opening_balance['Opening_Debit'] = df_opening_balance['Opening_Debit'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace(' ','0').str.replace('-','0')
    df_opening_balance['Opening_Credit'] = df_opening_balance['Opening_Credit'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace(' ','0').str.replace('-','0')
    df_opening_balance['Opening_Debit'] = df_opening_balance['Opening_Debit'].astype(float)
    df_opening_balance['Opening_Credit'] = df_opening_balance['Opening_Credit'].astype(float)
    df_opening_balance['Account No'] = df_opening_balance['Account No'].astype(str)
    df_opening_balance.head()


    df_transaction = pd.read_csv(getParser.getGLFile(file_dir, country_code), skiprows = 0, encoding = 'latin1') # skiprows = [0, 2, 5]
    #print(df_transaction.columns)
    for row_index, row in df_transaction.iterrows():
        if row['Particulars'] == 'Technical Services':
            #print(row_index)
            #print(df_transaction['Particulars'].iloc[row_index-1])
            df_transaction['Particulars'].iloc[row_index] = df_transaction['Particulars'].iloc[row_index-1]
    df_transaction.drop(['Unnamed: 2', 'Unnamed: 3'], axis=1, inplace=True, errors='ignore')
    df_transaction.dropna(subset=['Debit Amount', 'Credit Amount'], how='all', inplace=True)
    df_transaction['Date'].fillna(method='ffill', inplace=True)
    df_transaction['Vch Type'].fillna(method='ffill', inplace=True)
    df_transaction['Vch No.'].fillna(method='ffill', inplace=True)
    #df_transaction['Date'] =  pd.to_datetime(df_transaction['Date'], format='%d/%M/%y')
    #df_transaction.rename(columns = {'Particulars':'Account No'}, inplace = True)
    #df_transaction['Debit Amount'] = df_transaction['Debit Amount'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace('-','0').str.replace('Cr','0').str.replace('Dr','0').str.replace(' ','')
    #df_transaction['Credit Amount'] = df_transaction['Credit Amount'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace('-','0').str.replace('Cr','0').str.replace('Dr','0').str.replace(' ','')
    df_transaction['Debit Amount'] = df_transaction['Debit Amount'].astype(float)
    df_transaction['Credit Amount'] = df_transaction['Credit Amount'].astype(float)
    #df_transaction['Account No'] = df_transaction['Account No'].astype(str)
    df_transaction.head()


    df_opening_balance_groupby = df_opening_balance.groupby('Account')
    date_time = last_date
    #date_time = pd.to_datetime(date_time)
    flag = ''

    columns_ = df_opening_balance.columns.tolist()
    columns_.append('Vch Type')
    columns_.append('Vch No')

    # iterate over each group
    list_final = []
    for group_name, df_opening_balance_ in df_opening_balance_groupby:
        flag = df_opening_balance_['BS Classifications'].iloc[0]
        #print(flag)
        #if(group_name == '1-2120'):
        #print('Grouping for - '+group_name)
        #print(df_opening_balance.iloc[0].tolist())
        df_transaction_filtered = df_transaction[df_transaction['Particulars'].isin([group_name])]
        #df_global_tb_filtered = df_global_tb[df_global_tb['Grouping'].str.contains(group_name, case=False, na=False)]
        #print(df_global_tb_filtered)
        list_group = []
        list_temp = df_opening_balance_.iloc[0].tolist()
        list_temp.append(np.nan)
        list_temp.append(np.nan)
        list_group.append(list_temp)
        if len(df_transaction_filtered) > 0:
            #print(df_opening_balance.iloc[0].tolist())
            for row_index, row in df_transaction_filtered.iterrows():
                list_temp_ = df_opening_balance_.iloc[0].tolist()
                list_temp_[0] = row['Date']
                list_temp_[3] = row['Particulars']
                list_temp_[4] = row['Debit Amount']
                list_temp_[5] = row['Credit Amount']
    #             list_temp[6] = row['Vch Type']
    #             list_temp[7] = row['Vch No.']
                list_temp_.append(row['Vch Type'])
                list_temp_.append(row['Vch No.'])
                list_group.append(list_temp_)
        list_temp = df_opening_balance_.iloc[0].tolist()
        list_temp[0] = date_time
        list_temp[3] = 'Closing Balance'
        
        #print(columns_)
        #print(list_group)
        df_temp = pd.DataFrame(list_group, columns = columns_)
        closing_balance = df_temp['Opening_Debit'].sum() - df_temp['Opening_Credit'].sum()
        if (flag == 'PL'):
            
            # Apply condition for managing debit and credit amount
            list_temp_ = df_opening_balance_.iloc[0].tolist()
            for i in range(2, len(list_temp_)-1):
                list_temp_[i] = 'Profit or Loss'
            list_temp_[0] = date_time
            list_temp_[1] = '7000-10000'
            list_temp_[6] = '7000-10000'
            list_temp_[8] = flag
            if (closing_balance < 0):
                list_temp[5] = abs(closing_balance)
                list_temp[4] = 0.0
                list_temp_[4] = abs(closing_balance)
                list_temp_[5] = 0.0
            else:
                list_temp[5] = 0.0
                list_temp[4] = abs(closing_balance)
                list_temp_[4] = 0.0
                list_temp_[5] = abs(closing_balance)
            
            list_group.append(list_temp_)
        else:
            if (closing_balance < 0):
                list_temp[4] = abs(closing_balance)
                list_temp[5] = 0.0
            else:
                list_temp[4] = 0.0
                list_temp[5] = abs(closing_balance)
        list_group.append(list_temp)
        list_final.extend(list_group)
        #print(f' [INFO]: For account # {group_name}, Total Debit is: {df_temp["Opening_Debit"].sum()}, Total Cebit is: {df_temp["Opening_Credit"].sum()} and Closing Balance: {closing_balance}')
        #print(list_final)
        #break
            
    df_final = pd.DataFrame(list_final, columns = columns_)
    #df_final['Account No'] = df_final['Account No'].astype(str)
    #df_final['Account No'] = "'" + df_final['Account No']
    #df_final['Date'] =  pd.to_datetime(df_final['Date'], format='%d%m%Y:%H:%M:%S.%f')
    #df_final.to_csv('/Users/nvibhu/Documents/mozark/finance/Trial_Balance/Trial_Balance_IN.csv', mode='w', sep=',', encoding='utf-8', index=False)
    df_final_ = df_final.copy()

    df_customer = pd.read_csv(getParser.getCustomerFile(file_dir, country_code), encoding = 'latin1')

    df_final_.insert(len(df_final_.axes[1]), 'Customer Name', '', True)
    df_final_.insert(len(df_final_.axes[1]), 'Sales force', '', True)
    for row_index, row in df_customer.iterrows():
        df_final_filtered = df_final_[df_final_['Account'].str.contains(row['Customer Names'], case=False, na=False)]
        if (len(df_final_filtered) > 0):
            for row_index_, row_ in df_final_filtered.iterrows():
                df_final_.loc[row_index_, 'Customer Name'] = row['Customer Names']
                df_final_.loc[row_index_, 'Sales force'] = row['Sales force']
            
    df_final_.to_csv(getParser.getMasterFile(file_dir, country_code), mode='w', sep=',', encoding='utf-8', index=False)    
    df_final_.head()


            