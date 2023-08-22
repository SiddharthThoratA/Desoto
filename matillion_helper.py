import pandas as pd
from postgres_connect import init_connection
import pytz
from  datetime import date
from datetime import datetime,timedelta
import test_time as tt
 

#conn = init_connection()


def query_generator():
    conn = init_connection()
    
    pst = pytz.timezone('America/Los_Angeles')
    p_time = datetime.now(pst)
    run_date = p_time.strftime('%Y-%m-%d')
    
    #trunc(starttime) = to_char(convert_timezone('US/Pacific',sysdate),'yyyy-mm-dd')
    
    sql_query = pd.read_sql_query('''select id,jobname,status,starttime,endtime from "backup".audit_jobsummary_tbl where trunc(starttime) = to_char(convert_timezone('US/Pacific',sysdate),'yyyy-mm-dd');''',conn)
    df = pd.DataFrame(sql_query)
    return df

def color_status(val):
    color = 'red' if val=='FAILED' else 'green' if  val == 'SUCCESS' else 'yellow'
    return f'background-color: {color}'


def mtln_count_status(curr_df):
    running_process = curr_df[curr_df['status'] == 'RUNNING']
    etl_running_count = running_process['status'].count()
    
    failed_process = curr_df[curr_df['status'] == 'FAILED']
    etl_failed_count = failed_process['status'].count()
    
    # if etl_failed_count == 0:
    #     print("There is no any falied process")
    # elif etl_failed_count == 1:
    #     etl_name = failed_process['jobname'].values[0]
    #     print(etl_name)
    #     tt.send_msg_teams(etl_name)
    # else:
    #     etl_names = failed_process['script_name'].values.tolist()
    #     etl_names = ', '.join(etl_names)
    #     tt.send_msg_teams(etl_names)
    
    success_process = curr_df[curr_df['status'] == 'SUCCESS']
    etl_success_count = success_process['status'].count()
    
    return etl_running_count,etl_failed_count,etl_success_count 
