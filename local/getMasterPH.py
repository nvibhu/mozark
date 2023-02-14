import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import getParser

def getMasterPH(file_dir, country_code, last_date):

    print(f' [INFO] [{country_code}]: Getting files from dir - {getParser.getOpeningTBFile(file_dir, country_code)}')

    df_opening_balance = pd.read_csv(getParser.getOpeningTBFile(file_dir, country_code), encoding = 'latin1')
    #df_opening_balance['Date'] =  pd.to_datetime(df_opening_balance['Date']) #format='%d%b%Y:%H:%M:%S.%f'
    #df_opening_balance['Date'] =  pd.to_datetime(df_opening_balance['Date'], format='%d/%m/%y')
    df_opening_balance['Opening_Debit'] = df_opening_balance['Opening_Debit'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace(' ','0').str.replace('-','0')
    df_opening_balance['Opening_Credit'] = df_opening_balance['Opening_Credit'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace(' ','0').str.replace('-','0')
    df_opening_balance['Opening_Debit'] = df_opening_balance['Opening_Debit'].astype(float)
    df_opening_balance['Opening_Credit'] = df_opening_balance['Opening_Credit'].astype(float)
    df_opening_balance['Account No'] = df_opening_balance['Account No'].astype(str)
    df_opening_balance['RC Code'] = df_opening_balance['RC Code'].fillna('NA')
    df_opening_balance.head()


    df_transaction = pd.read_csv(getParser.getGLFile(file_dir, country_code), skiprows = 10, encoding = 'latin1')
    df_transaction.rename(columns = {'DOC DATE':'Date', 'DOC NO':'Doc No', 'PARTICULARS':'Particulars', 'RC CODE':'RC Code',
                                    'ACCT CODE':'Account No', 'DEBIT':'Debit Amount', 
                                    'CREDIT':'Credit Amount'}, inplace = True)
    df_transaction.dropna(subset=['Date'], inplace=True)
    df_transaction['Date'] =  pd.to_datetime(df_transaction['Date'], format='%m/%d/%Y')
    df_transaction = df_transaction[~df_transaction['Particulars'].isin(['Beginning Balance'])]

    df_transaction['Debit Amount'] = df_transaction['Debit Amount'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace(' ','0').str.replace('-','0')
    df_transaction['Credit Amount'] = df_transaction['Credit Amount'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace(' ','0').str.replace('-','0')
    df_transaction['Debit Amount'] = df_transaction['Debit Amount'].astype(float)
    df_transaction['Credit Amount'] = df_transaction['Credit Amount'].astype(float)
    df_transaction['Account No'] = df_transaction['Account No'].astype(str)
    df_transaction['RC Code'] = df_transaction['RC Code'].fillna('NA')
    df_transaction.head()

    df_opening_balance_groupby = df_opening_balance.groupby(['Account No', 'RC Code'])
    date_time = last_date
    #date_time = pd.to_datetime(date_time)
    flag = ''

    columns_ = df_opening_balance.columns.tolist()
    #columns_.append('RC Code')
    columns_.append('Doc No')

    # iterate over each group
    list_final = []
    for group_name, df_opening_balance_ in df_opening_balance_groupby:
        #print(group_name[0],group_name[1],group_name)
        flag = df_opening_balance_['BS Classifications'].iloc[0]
        #print(flag)
        #if(group_name == '1-2120'):
        #print('Grouping for - '+group_name)
        #print(df_opening_balance.iloc[0].tolist())
        df_transaction_filtered = df_transaction[df_transaction['Account No'].isin([group_name[0]]) & df_transaction['RC Code'].isin([group_name[1]])]
        #df_global_tb_filtered = df_global_tb[df_global_tb['Grouping'].str.contains(group_name, case=False, na=False)]
        #print(df_global_tb_filtered)
        list_group = []
        list_temp = df_opening_balance_.iloc[0].tolist()
        list_temp.append(np.nan)
        #list_temp.append(np.nan)
        list_group.append(list_temp)
        if len(df_transaction_filtered) > 0:
            #print(df_opening_balance.iloc[0].tolist())
            for row_index, row in df_transaction_filtered.iterrows():
                list_temp_ = df_opening_balance_.iloc[0].tolist()
                list_temp_[0] = row['Date']
                list_temp_[3] = row['Particulars']
                list_temp_[4] = row['Debit Amount']
                list_temp_[5] = row['Credit Amount']
                list_temp_[len(list_temp_)-1] = row['RC Code']
                #list_temp_.append(row['RC Code'])
                list_temp_.append(row['Doc No'])
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

    df_customer = pd.read_csv(getParser.getCustomerFile(file_dir, country_code), encoding = 'latin1')
    df_merged = pd.merge(df_final, df_customer, how='left', left_on=['RC Code'], right_on=['RC Code'])
    df_merged.to_csv(getParser.getMasterFile(file_dir, country_code), mode='w', sep=',', encoding='utf-8', index=False)
    df_merged.head()

