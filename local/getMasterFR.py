import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import getParser

def getMasterFR(file_dir, country_code, last_date):

    print(f' [INFO] [{country_code}]: Getting files from dir - {getParser.getOpeningTBFile(file_dir, country_code)}')

    df_transaction = pd.read_csv(getParser.getGLFile(file_dir, country_code), encoding = 'latin1') #encoding = 'ISO-8859-1'
    df_transaction.rename(columns = {'Jal.':'Jal', 'Pièce / Lig.':'Piece', 'Libellé':'Libelle', 'Référence':'Reference',
                                    'ACCT CODE':'Account No', 'Débit':'Debit Amount', 'Crédit':'Credit Amount',
                                    'Lettr.':'Lettr'}, inplace = True)

    print(df_transaction.columns)
    #df_transaction['Date'] = df_transaction['Date'].astype(str)
    df_transaction['Date'] =  pd.to_datetime(df_transaction['Date']) #format='%d%m%y'
    #df_transaction['Debit Amount'] = df_transaction['Debit Amount'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','')
    #df_transaction['Credit Amount'] = df_transaction['Credit Amount'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','')
    df_transaction['Debit Amount'] = df_transaction['Debit Amount'].astype(float)
    df_transaction['Credit Amount'] = df_transaction['Credit Amount'].astype(float)
    df_transaction.head(20)

    list_final = []
    #list_temp = []
    account_memo = []
    for row_index, row in df_transaction.iterrows():
        if row['Date'] == row['Date']:
            list_temp = []
            if len(account_memo) > 0:
                #if df_transaction.iloc[row_index+1]['Date'] == df_transaction.iloc[row_index+1]['Date']:
                #list_temp.append(row['Date'], row['Jal'], row['Piece'], account_memo[0], account_memo[0],\
                #                 row['Reference'], row['Debit Amount'], row['Credit Amount'] )
                list_row = []
                list_row = row.tolist()
                list_row.append(str(account_memo[0]))
                list_row.append(account_memo[1])
                list_temp.append(list_row)
                #print(list_temp)
            else:
                account_memo = df_transaction.iloc[row_index-2]['Libelle'].split('   ')
                #list_temp.append(row['Date'], row['Jal'], row['Piece'], account_memo[0], account_memo[0],\
                #                 row['Reference'], row['Debit Amount'], row['Credit Amount'] )
                list_row = []
                list_row = row.tolist()
                list_row.append(str(account_memo[0]))
                list_row.append(account_memo[1])
                list_temp.append(list_row)
                #print(list_temp)
                #print(row_index, row['Date'], row['Libelle'])
                
                
            list_final.extend(list_temp)    
        else:
            #list_temp = []
            account_memo = []
            #print('------------------------------')
            
    #print(list_final)   

    list_columns = df_transaction.columns.tolist()
    list_columns.append('Account No')
    list_columns.append('Account')
    #print(list_columns)
    df_transaction = pd.DataFrame(list_final, columns = list_columns)
    df_transaction.rename(columns = {'Libelle':'Particulars'}, inplace = True)


    df_opening_balance = pd.read_csv(getParser.getOpeningTBFile(file_dir, country_code), encoding = 'latin1')
    #df_opening_balance['Date'] =  pd.to_datetime(df_opening_balance['Date']) #format='%d%b%Y:%H:%M:%S.%f'
    df_opening_balance['Date'] =  pd.to_datetime(df_opening_balance['Date'], format='%d/%m/%y')
    df_opening_balance['Opening_Debit'] = df_opening_balance['Opening_Debit'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace(' ','')
    df_opening_balance['Opening_Credit'] = df_opening_balance['Opening_Credit'].str.replace('RM','').str.replace('S','').str.replace('$','').str.replace('U','').str.replace('E','').str.replace('R','').str.replace(',','').str.replace(' ','')
    #print(df_opening_balance['Opening_Debit'].unique())
    df_opening_balance['Opening_Debit'] = df_opening_balance['Opening_Debit'].astype(float)
    df_opening_balance['Opening_Credit'] = df_opening_balance['Opening_Credit'].astype(float)
    df_opening_balance['Account No'] = df_opening_balance['Account No'].astype(str)
    df_opening_balance.head()


    df_opening_balance_groupby = df_opening_balance.groupby('Account No')
    date_time = last_date
    date_time = pd.to_datetime(date_time)
    flag = ''

    columns_ = df_opening_balance.columns.tolist()
    columns_.append('Jal')
    columns_.append('Piece')
    columns_.append('Reference')
    columns_.append('Solde')
    columns_.append('Lettr')

    # iterate over each group
    list_final = []
    for group_name, df_opening_balance_ in df_opening_balance_groupby:
        flag = df_opening_balance_['BS Classifications'].iloc[0]
        #print(flag)
        #if(group_name == '1-2120'):
        #print('Grouping for - '+group_name)
        #print(df_opening_balance.iloc[0].tolist())
        df_transaction_filtered = df_transaction[df_transaction['Account No'].isin([group_name])]
        #df_global_tb_filtered = df_global_tb[df_global_tb['Grouping'].str.contains(group_name, case=False, na=False)]
        #print(df_global_tb_filtered)
        list_group = []
        list_temp = df_opening_balance_.iloc[0].tolist()
        list_temp.append(np.nan)
        list_temp.append(np.nan)
        list_temp.append(np.nan)
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
                list_temp_.append(row['Jal'])
                list_temp_.append(row['Piece'])
                list_temp_.append(row['Reference'])
                list_temp_.append(row['Solde'])
                list_temp_.append(row['Lettr'])
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
    df_final['Date'] =  pd.to_datetime(df_final['Date'], format='%d-%m-%Y')

    #df_customer = pd.read_csv('/Users/nvibhu/Documents/mozark/finance/Trial_Balance/Customer Name/Customer_SGP.csv', 
    #                             encoding = 'latin1')
    #df_merged = pd.merge(df_final, df_customer, how='left', left_on=['Job'], right_on=['Job'])
    df_final.to_csv(getParser.getMasterFile(file_dir, country_code), mode='w', sep=',', encoding='latin1', index=False)
    df_final.head()


            


            