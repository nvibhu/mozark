
def getOpeningTBFile(file_dir, country_code):
    file_path = file_dir+'/Input/Opening TB/Opening_Balance_'+country_code+'.csv'
    #print(file_path)
    return file_path

def getGLFile(file_dir, country_code):
    file_path = file_dir+'/Input/General Ledgers/GL_'+country_code+'.csv'
    #print(file_path)
    return file_path

def getCustomerFile(file_dir, country_code):
    file_path = file_dir+'/Input/Customer Name/Customer_'+country_code+'.csv'
    #print(file_path)
    return file_path

def getMasterFile(file_dir, country_code):
    file_path = file_dir+'/Master/Master_'+country_code+'.csv'
    #print(file_path)
    return file_path

def getMasterFileAll(file_dir, country_code='All'):
    file_path = file_dir+'/Master/Master_'+country_code+'.csv'
    #print(file_path)
    return file_path

def getGroupWiseExpenseReport(file_dir, country_code='All'):
    file_path = file_dir+'/Output/Group_Wise_Expense_Report_'+country_code+'.csv'
    #print(file_path)
    return file_path

def getSFChronoFile(file_dir, country_code):
    file_path = file_dir+'/Input/Salesforce/Complete Report-FY 23 with Chrono - Exp.csv'
    #print(file_path)
    return file_path

def getSFSegmentFile(file_dir, country_code):
    file_path = file_dir+'/Input/Salesforce/Accounts Report by Segment.csv'
    #print(file_path)
    return file_path

def getSFChronoSegmentFile(file_dir, country_code):
    file_path = file_dir+'/Output/Complete Report-FY 23 with Chrono and Segments.csv'
    #print(file_path)
    return file_path

def getCOSWithoutRevenueFile(file_dir, country_code):
    file_path = file_dir+'/Output/COS_Without_Revenue.csv'
    #print(file_path)
    return file_path

def getCOSGreaterThanRevenueFile(file_dir, country_code):
    file_path = file_dir+'/Output/COS_Greater_Than_Revenue.csv'
    #print(file_path)
    return file_path

def getSFCOSFile(file_dir, country_code, report_type):
    file_path = file_dir+'/Output/SF_COS_'+report_type+'.csv'
    #print(file_path)
    return file_path

def getGraphMarginReportFile(file_dir, country_code, report_type):
    file_path = file_dir+'/Output/Graph_Margin_Report_'+report_type+'.csv'
    #print(file_path)
    return file_path