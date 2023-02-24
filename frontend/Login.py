import requests
import streamlit as st



## 
def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

# Create an empty container
placeholder = st.empty()

actual_email = "admin"
actual_password = "admin"
session = requests.Session()

# Insert a form in the container
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False
if st.session_state["authentication_status"] == False:
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        username = st.text_input("UserName")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    if submit:
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        url = 'http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/user/login'
        myobj = {'username': username ,'password': password }
        x_status = requests.post(url, data = myobj).status_code
        # print(x_status)
        st.write(x_status)
        if x_status == 200:
            x = requests.post(url, data = myobj).json()    
            st.success("Login successful")
            log_username = x['username']
            log_token = x['access_token']
            # goes_ui.goes_ui()

            # print(log_username)
            # print(log_token)
        # Initialization of session state:
        
            st.session_state["authentication_status"] = log_token
            st.success("Login successful") 
            st.write(x)
            # if logout:
            #     st.session_state["authentication_status"] == False
            #     placeholder.empty()
        elif x_status == 404 or x_status == 401:
            # if 'shared' not in st.session_state:
            st.session_state["authentication_status"] == False
            st.error("Login failed ... Invalid credentials")
        # if st.session_state["authentication_status"] == log_token:
        #     st.success("Login successful") 
        # else:
        #     pass
else:
    st.header("User logged in Successfully")
    logout = st.button("Log Out")
    if logout:
        st.session_state["authentication_status"] == False
        st.header("Logged Out Successfully")
# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title('Some content')
# elif st.session_state["authentication_status"] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] == None:
#     st.warning('Please enter your username and password')


