## Library Imports
import pandas as pd
import streamlit as st
import datetime
import streamlit as st
from datetime import date
import requests
import re
def day_of_year(month, day):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        total_days = 0
        for i in range(month - 1):
            total_days += days_in_month[i]
        total_days += day
        if(len(str(total_days))==1):
            total_days = '00'+str(total_days)
        elif(len(str(total_days))==2):
            total_days = '0'+ str(total_days)
        return total_days
hours_list = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
sd = pd.read_fwf('https://www.ncei.noaa.gov/access/homr/file/nexrad-stations.txt')
sd = sd.drop(index = 0,axis = 0)
station_id = sd['ICAO'].astype(str).to_list()


def nexrad_ui():

    # Check if 'key' already exists in session_state
    # If not, then initialize it
    # if 'key' not in st.session_state:
    #     st.session_state['key'] = 'value'

    # # Session State also supports the attribute based syntax
    # if 'key' not in st.session_state:
    #     st.session_state.key = 'value'

    # # Store the initial value of widgets in session state
    # if "visibility" not in st.session_state:
    #     st.session_state.visibility = "visible"
    #     st.session_state.disabled = False

    # st.title('This is a title')
    st.title('Search By _File_ : :blue[NEXRAD] Data')
    st.sidebar.markdown("# NexRad Map")
    st.subheader("Please select your Search Criteria")
    st.markdown("# NexRad UI")
  
    

    #----------------------------------------------------------
    d = st.date_input(
        "Select the date",
        value = datetime.date(2023, 2, 4),
        min_value= datetime.date(2022, 1, 1), max_value=date.today())
    st.write('Your Selection is:', d)
    day_nexrad = d.day
    if(len(str(day_nexrad))==1):
        day_nexrad = '0'+str(day_nexrad)
    month_nexrad = d.month
    if(len(str(month_nexrad))==1):
        month_nexrad = '0'+str(month_nexrad)
    year_nexrad = d.year

    station = st.selectbox(
        'Select the required Station',
        station_id)
    # Log().i(station)

    st.write('You selected:', station)
    
    ## API 'GET' CALL
    token = st.session_state["authentication_status"]
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'stationId':str(station),'day': day_nexrad,'year':year_nexrad,'month':month_nexrad}
    stcheck = requests.get("http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/nexrad/files", params = payload, headers=headers)
    output =  stcheck.json()
    # print(output)
    output_files = output['all_files']
    # output_files = nexs3.get_all_nexrad_file_name_by_filter(str(year_nexrad),str(month_nexrad), str(day_nexrad),str(station))
    # output_files = nexs3.get_all_nexrad_file_name_by_filter('2023', '02', '04', 'KABR')
    if not output_files:
        st.markdown('**:red[data NOT available for given Inputs]**')
    else:
        st.write('')
    # print(output_files)
    sl_file = st.selectbox('Select the required file for Link',output_files)
    # Log().i(sl_file)
    ## Button code :

    if st.button('Generate Link', key ='nexrad_filed_search'):
        ### API 'POST' CALL
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        url = 'http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/nexrad/generate/aws-link'
        myobj = {'station_id': str(station) ,'year': year_nexrad ,'day': day_nexrad,'month': month_nexrad,'file_name': str(sl_file)}
        nexrad_status = requests.post(url, json = myobj,headers = headers).status_code
        if nexrad_status == 201:
            st.success("fetched file url")
            x = requests.post(url, json = myobj, headers=headers).json()    
            print(x)
            team_link = x['team_link']
            nexrad_link = x['nexrad_link']
        # team_link, goes_link = s3.get_geos_aws_link(station,str(year_goes),str(doy), str(hour),str(sl_file))
            st.write('Our Link')
            st.write(team_link)
            st.write('NexRad Link')
            st.write(nexrad_link)
        elif nexrad_status == 401 or nexrad_status == 404:
            st.write("Input is Invalid")
    else:
        st.write(' ')

    ##############################################################
    st.title('Search your NEXRAD file : :NEXRAD Data')
    st.subheader("Please input your File Name")
    # Text input :

    file_input = st.text_input('File Name','' )


 ## Button code :
    regex = re.compile(r'K[A-Z]{3}[0-9]{8}_[0-9]{6}(_V06_MDM)?')
    match = regex.match(file_input)
    if st.button('Generate the link',key = 'nexrad_file_search'):
        if match:
            # print("yes checked")
            # file_name = s3.get_aws_link_by_filename(file_input)
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
            result_status = requests.post(f"http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/nexrad/generate/aws-link-by-filename/{file_input}",headers = headers).status_code
            if result_status == 201:
            
                result = requests.post(f"http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/nexrad/generate/aws-link-by-filename/{file_input}",headers = headers).json()
                file_name = result['bucket_link']
                st.write(file_name)
            elif result_status!= 201:
                st.markdown('**:red[Input file name does not exist]**') 
        elif not match:
            st.markdown('**:red[Input format not supported]**')

    else:
        st.write(' ')


if "authentication_status" not in st.session_state:
   st.session_state["authentication_status"] = False
if st.session_state["authentication_status"] == False:
      st.subheader("Please Login before use")
else:
    nexrad_ui()
