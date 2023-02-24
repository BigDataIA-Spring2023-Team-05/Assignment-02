## Library Imports
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

def goes_ui():
   
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
    st.title('Search By _File_ : :blue[GOES] Data')
    st.sidebar.markdown("# :blue[GOES] Search")
    st.subheader("Please select your Search Criteria")
    st.markdown("# GOES UI")


    station = 'ABI-L1b-RadC'
    st.write('You selected:', station)
    d = st.date_input(
        "Select the date",
        # value = datetime.date(2022, 7, 28),
        min_value= datetime.date(2022, 7, 28), max_value=date.today())
    st.write('Your Selection is:', d)
    day_goes = d.day
    month_goes = d.month
    year_goes = d.year
    # Log().i(day_goes)
    # Log().i(month_goes)
    # Log().i(year_goes)

    # print('day' + ':'+ str(day_goes))
    # print('month' + ':'+ str(month_goes))
    ## Creating date of the year:

    doy = day_of_year(month_goes,day_goes)
    print(doy)
    print('day of year' + ':'+ str(doy))
    hour = st.selectbox(
        'Select the required Hour',
        hours_list)

    st.write('You selected:', hour)
    # url = 'http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/goes/files'
    # myobj = {'username': username ,'password': password }
    # x = requests.post(url, data = myobj).json()

    ## GET API CALL
    token = st.session_state["authentication_status"]
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'station':'ABI-L1b-RadC','day':doy,'year':year_goes,'hour':hour}
    output = requests.get("http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/goes/files", params = payload, headers=headers).json()
    # print(output)
    output_files = output['all_files']

    # print(output_files)



    if not output_files:
        st.markdown('**:red[data NOT available for given Inputs]**')
    else:
        st.write('')
    
    sl_file = st.selectbox('Select the required file for Link',output_files)
    # Log().i(sl_file)
    ## Button code :

    # if st.button('Search',key = 'goes_file_output'):
    #     fo1 = s3.get_all_geos_file_name_by_filter(station, str(year_goes),str(doy), str(hour))
    #     print(fo1)
        
    # sl_file = st.selectbox('Select the required file for Link',fo1)
    if st.button('Generate Link', key ='goes_filed_search'):
        ### GOES API POST CALL
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        url = 'http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/goes/generate/aws-link'
        myobj = {'station': 'ABI-L1b-RadC' ,'year': year_goes ,'day': doy,'hour':hour,'file_name': str(sl_file)}
        # print(myobj)
        goes_status = requests.post(url, json= myobj,headers=headers).status_code
        print(goes_status)
        if goes_status == 201:
            st.success("fetched file url")
            x = requests.post(url, json = myobj, headers=headers).json()    
            print(x)
            team_link = x['team_link']
            goes_link = x['goes_link']
        # team_link, goes_link = s3.get_geos_aws_link(station,str(year_goes),str(doy), str(hour),str(sl_file))
            st.write('Our Link')
            st.write(team_link)
            st.write('GOES Link')
            st.write(goes_link)
        elif goes_status == 401 or goes_status == 404:
            st.write("Input is Invalid")
        # o_df = pd.DataFrame(data = file_output, columns = ['File Name'])
        # l = []
        # for f in file_output:
        #     temp = s3.get_aws_link_by_filename(f)
        #     l.append(temp)
        # print(l)
        # l_df = pd.DataFrame(data = l,columns = ['File Link'])
        # fdf = o_df.join(l_df)
        # print(fdf)
        # st.write(fdf)
    else:
        st.write(' ')

    ##############################################################
    st.title('Search By _FileName_ : :blue[GOES] Data')
    st.subheader("Please input your File Name")
    # Text input :

    file_input = st.text_input('File Name','' )
    # Log().i(file_input)

    ## Button code :
    regex = re.compile(r'(OR)_(ABI)-(L\d+b)-(Rad[A-Z]?)-([A-Z]\dC\d{2})_(G\d+)_(s\d{14})_(e\d{14})_(c\d{14}).nc')
    match = regex.match(file_input)
    if st.button('Generate the link',key = 'goes_file_search'):
        if match:
            # print("yes checked")
            # file_name = s3.get_aws_link_by_filename(file_input)
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
            result_status = requests.post(f"http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/goes/generate/aws-link-by-filename/{file_input}",headers = headers).status_code
            if result_status == 201:
            
                result = requests.post(f"http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/goes/generate/aws-link-by-filename/{file_input}",headers = headers).json()
                file_name = result['bucket_link']
                st.write(file_name)
            elif result_status!= 201:
                st.markdown('**:red[Input file does not exist]**') 
        elif not match:
            st.markdown('**:red[Input format not supported]**')

    else:
        st.write(' ')



if "authentication_status" not in st.session_state:
   st.session_state["authentication_status"] = False
if st.session_state["authentication_status"] == False:
      st.subheader("Please Login before use")
else:
      goes_ui()
