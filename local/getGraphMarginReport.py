import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import getParser
import getParameter

def getGraphMarginReport(file_dir, country_code, report_type):
    
    print(f' [INFO] [Graph]: Generating margin report for graph - {getParser.getSFCOSFile(file_dir, country_code, report_type)}')

    # Generate graph margin report
    df_graph = pd.read_csv(getParser.getSFCOSFile(file_dir, country_code, report_type), encoding = 'latin1')
    ##df_graph = pd.read_csv('/Users/nvibhu/Documents/mozark/finance/Trial_Balance/Complete_Report_SF_GL_Quarter.csv', encoding = 'latin1')
    #df_graph['Date_x'] =  pd.to_datetime(df_graph['Date'])
    list_col = ['Account Name: Region', 'Account Name', 'Type', 'Segment', 'Industry', 'Account Owner', 'Client Name', \
    'Gross Revenue', 'Net Revenue', 'Recurring Rev', 'PassThrough', 'Cost_Of_Sales', 'Cost_Of_Sales_Quarter',
    'Gross_Margin']
    df_graph = df_graph[list_col].copy()
    #print(df_graph['Account Name'].count())

    df_final_graph = pd.DataFrame()
    frames = []
    for col_name in df_graph.columns[-7:]:
        print('for column - ', col_name)
        df_temp = df_graph[df_graph.columns[:-7]].copy()
        df_temp.insert(len(df_temp.axes[1]), 'KPI_Type', col_name)
        df_temp.insert(len(df_temp.axes[1]), 'Value', df_graph.pop(col_name))
        #print(df_temp)
        frames.append(df_temp)
        #break
        
    df_final_graph = pd.concat(frames)
    ##df_final_graph.to_csv('/Users/nvibhu/Documents/mozark/finance/Trial_Balance/Margin_Report.csv', mode='w', sep=',', encoding='utf-8', index=False)
    df_final_graph.to_csv(getParser.getGraphMarginReportFile(file_dir, country_code, report_type), mode='w', sep=',', encoding='utf-8', index=False)

    #print(df_final_graph['Account Name'].count())
    #df_final_graph.head()

