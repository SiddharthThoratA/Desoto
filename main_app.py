#importing require modules
import streamlit as st
import pandas as pd
import numpy as np
import script_helper as sh
import matillion_helper as mh
from PIL import Image
from schedule import every, repeat, run_pending
import schedule
import time
import datetime
import pytz
from postgres_connect import init_connection

st.sidebar.header("PST DATE & TIME")
#time_date=st.write(datetime.datetime.now())
pst = pytz.timezone('America/Los_Angeles')
p_time = datetime.datetime.now(pst)
date_time = p_time.strftime('%Y/%m/%d %H:%M:%S')
date_time = '<p style="font-family:Courier; color:black; font-size: 20px;"><b>{}</b></p>'.format(date_time)

#st.sidebar.markdown("PST_DATE TIME: ",date_time)
st.sidebar.markdown(date_time, unsafe_allow_html=True)

#Desoto image 
image = Image.open('desoto_logo.png')
#width = 700, 280
st.sidebar.image(image,width=280)

#Keep header leftside below the image
st.sidebar.title("Process Monitoring Dashboard DeSoto Technologies")


#main function for webpage
def main():
    #Provide options for selection
    user_menu=st.sidebar.selectbox(
        'Select an option',
        ('ALL','Matillion Jobs Status','Scripts Status')
    )

    #Giving Page name
    #st.header("Dashboard")
    
    #if user select script status option
    if user_menu == 'Scripts Status':        
        st.subheader("Script Status")
        st.button("Refresh Program",on_click=sh.clear_cache)
        script_df = sh.query_generator()
    
        #st.dataframe(script_data)
        #script_df=st.dataframe(script_data.style.applymap(sh.color_status, subset=['status']))
        ##script_df=script_data.style.applymap(sh.color_status, subset=['status'])
        ##st.dataframe(script_df)
    
        #print(color_status)
    
        ##script_status=script_df['status'].unique().tolist()
        ##script_status.insert(0,'Overall')
        
        #script_status.sort()
        
        ##freq=script_df['frequency'].unique().tolist()
        ##freq.insert(0,'Overall')
        
    
        ##freq_selected = st.sidebar.selectbox('Select frequency:',freq)
        ##status_selected = st.sidebar.selectbox('Select status:',script_status)
        
        filter_data = sh.fetch_selected_data(script_df)
        filter_data=filter_data.style.applymap(sh.color_status, subset=['status'])
        st.dataframe(filter_data)

    elif user_menu == 'Matillion Jobs Status':
        st.header("Matillion Jobs Status")
        matillion_data = mh.query_generator()
        #st.dataframe(script_data)
        st.dataframe(matillion_data.style.applymap(mh.color_status, subset=['status']))
        #print(color_status)
    
    elif user_menu == 'ALL':
        st.header("Process status")
        st.button("Refresh Program",on_click=sh.clear_cache)
        
        curr_df = sh.query_generator()
        running_counts,failed_count,Long_running_count = sh.count_status(curr_df)
        
        mtln_curr_df = mh.query_generator()
        etl_running_count,etl_failed_count,etl_success_count = mh.mtln_count_status(mtln_curr_df)
        
        tab1, tab2 = st.tabs(["Total Running Jobs", "Total completed jobs"])
        
        with tab1:
    
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Scripts")
                st.write('Current Running processes: ')
                s_data = running_counts
                original_title = '<p style="font-family:Courier; color:black; font-size: 30px;"><b>{}</b></p>'.format(s_data)
                st.markdown(original_title, unsafe_allow_html=True)
                
                st.write('Long Running processes: ')
                l_data = Long_running_count
                original_title = '<p style="font-family:Courier; color:black; font-size: 30px;"><b>{}</b></p>'.format(l_data)
                st.markdown(original_title, unsafe_allow_html=True)
                
                st.write('Total Failed Scripts: ')
                failed_s = failed_count
                original_title = '<p style="font-family:Courier; color:red; font-size: 30px;"><b>{}</b></p>'.format(failed_s)
                st.markdown(original_title, unsafe_allow_html=True)
                
                
            with col2:
                st.subheader("Matillion Jobs")
                st.write('Total Success Jobs: ')
                success_m = etl_success_count
                original_title = '<p style="font-family:Courier; color:red; font-size: 30px;"><b>{}</b></p>'.format(success_m)
                st.markdown(original_title, unsafe_allow_html=True)
                
                st.write('Current Running processes: ')
                running_m = etl_running_count
                original_title = '<p style="font-family:Courier; color:black; font-size: 30px;"><b>{}</b></p>'.format(running_m)
                st.markdown(original_title, unsafe_allow_html=True)
                
                st.write('Total Failed Jobs: ')
                failed_m = etl_failed_count
                original_title = '<p style="font-family:Courier; color:red; font-size: 30px;"><b>{}</b></p>'.format(failed_m)
                st.markdown(original_title, unsafe_allow_html=True)
        
        with tab2:
            st.write('Jesta_15min_wrapper.sh: {}/60'.format(s_data))
            
        
        #matillion_data = mh.query_generator()
        #st.dataframe(script_data)
        #st.dataframe(matillion_data.style.applymap(mh.color_status, subset=['status']))

if __name__ == "__main__":
    main()
   