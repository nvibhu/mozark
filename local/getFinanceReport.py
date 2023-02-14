import json
import requests
import pandas as pd
import numpy as np
import os,sys
import re,ast
import calendar
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import concurrent.futures
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings("ignore")

from getMasterMY import getMasterMY
from getMasterSGP import getMasterSGP
from getMasterFR import getMasterFR
from getMasterPH import getMasterPH
from getMasterIN import getMasterIN

if __name__ == '__main__':
    print ("[INFO]: Mozark Financial Report")

    try :
        file_dir = sys.argv[1]
        last_date = sys.argv[2]
    except:
        print("Mandate parameter for file directory is missing(/../../)")
        #print("Defaulting to /mozark")
        #file_dir=''

    master_my = getMasterMY(file_dir, 'MY', last_date)
    master_sgp = getMasterSGP(file_dir, 'SGP', last_date)
    master_fr = getMasterFR(file_dir, 'FR', last_date)
    master_ph = getMasterPH(file_dir, 'PH', last_date)
    master_in = getMasterIN(file_dir, 'IN', last_date)


    # # Apply parallel processing for all the files
    # with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
    #     print(f' Input Artifacts -> {json.dumps(input_artifacts)}')
    #     fa_patching_data = executor.submit(faPatching_, fa_patching, fa_version, release_set_id, release_set_namespace, is_patch_direct_apply, tenancy, region, env_family, compartment_id, date_time_now, cm_link)
    #     fa_update_data = executor.submit(faUpdate_, fa_update, fa_version, release_set_id, release_set_namespace,  source_fa_version, source_release_set_id, source_release_set_namespace, is_patch_direct_apply, tenancy, region, env_family, compartment_id, date_time_now, cm_link)
    #     p2t_refresh_data = executor.submit(p2tRefresh_, p2t_refresh, fa_version, release_set_id, release_set_namespace, tenancy, region, env_family, compartment_id, date_time_now, cm_link)
    #     tshirt_resize_data =  executor.submit(tShirtResize_, t_shirt_resize, ate_testing, fa_version, release_set_id, release_set_namespace, is_patch_direct_apply, tenancy, region, env_family, compartment_id, date_time_now, cm_link)

    #     #executor.map(get_patchBundle_data_v1, env_type, csv_op_file)
    #     #executor.map(get_patchBundle_data_v2, env_type, csv_op_file)





