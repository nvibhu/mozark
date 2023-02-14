
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