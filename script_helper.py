import streamlit as st
import pandas as pd
from postgres_connect import init_connection
from  datetime import date
from datetime import datetime,timedelta
import time
import pytz
from schedule import every, repeat, run_pending
#import test_time


#curr_date = ''

#run_date = '2023-05-18'



#print(sql)

def query_generator():
    conn = init_connection()
    
    pst = pytz.timezone('America/Los_Angeles')
    p_time = datetime.now(pst)
    run_date = p_time.strftime('%Y-%m-%d')
    
    #run_date = date.today()
    #run_date = run_date.strftime('%Y-%m-%d')
    
    #run_date=date=datetime.now() - timedelta(6)
    #run_date = run_date.strftime('%Y-%m-%d')
    
    sql = "select script_name,frequency ,status,starttime,endtime  from backup.script_audit_jobsummary_tbl_st where trunc(starttime) = 'curr_date' order by starttime desc;"
    sql = sql.replace('curr_date',run_date)
    
    sql_query = pd.read_sql_query(sql,conn)
    df = pd.DataFrame(sql_query)
    return df
    
    
#while True:
##    run_pending()
 #   time.sleep(1)
    
def color_status(val):
    color = 'red' if val=='FAILED' else 'green' if  val == 'SUCCESS' else 'yellow' if val == 'LONG_RUNNING' else 'blue'
    return f'background-color: {color}'


def clear_cache():
    st.cache_resource.clear()


#temp_df = pd.DataFrame()

def fetch_selected_data(script_df):
    
    script_status=script_df['status'].unique().tolist()
    script_status.insert(0,'Overall')
    freq=script_df['frequency'].unique().tolist()
    freq.insert(0,'Overall')
    
    freq_selected = st.sidebar.selectbox('Select frequency:',freq)
    status_selected = st.sidebar.selectbox('Select status:',script_status)
    
    if freq_selected == 'Overall' and status_selected == 'Overall':
        temp_df = script_df
    elif freq_selected == 'Overall' and status_selected != 'Overall':
        temp_df = script_df[script_df['status'] == status_selected]
    elif freq_selected != 'Overall' and status_selected == 'Overall':
        temp_df =  script_df[script_df['frequency'] == freq_selected]
    elif freq_selected != 'Overall' and status_selected != 'Overall':
        temp_df = script_df[(script_df['frequency'] == freq_selected) & (script_df['status'] == status_selected)]    
    return temp_df
    
def count_status(curr_df):
    running_scripts = curr_df[curr_df['status'] == 'RUNNING']
    running_count = running_scripts['status'].count()
    
    failed_scripts = curr_df[curr_df['status'] == 'FAILED']
    failed_count = failed_scripts['status'].count()
    
    if failed_count == 0:
        print("There is no any falied process")
    elif failed_count == 1:
        script_name = failed_scripts['script_name'].values[0]
        print(script_name)
        #test_time.send_msg_teams(script_name)
    else:
        script_name = failed_scripts['script_name'].values.tolist()
        script_names = ', '.join(script_name)
        #test_time.send_msg_teams(script_names)
    
    Long_running_scripts = curr_df[curr_df['status'] == 'LONG_RUNNING']
    Long_running_count = Long_running_scripts['status'].count()
    
    return running_count,failed_count,Long_running_count
    
      

#def color_helper(script_data):
    #st.dataframe(script_data.style.applymap(script_data.color_status(), subset=['status']))
##    script_data=script_data.style.applymap(script_data.color_status(), subset=['status'])
 #   return script_data