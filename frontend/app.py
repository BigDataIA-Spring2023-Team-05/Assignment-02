import pandas as pd
import numpy as mp
import requests
import streamlit as st
import datetime
import streamlit as st
from datetime import datetime, timedelta
from typing import Union
import streamlit_authenticator as stauth
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
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
with placeholder.form("login"):
    st.markdown("#### Enter your credentials")
    username = st.text_input("UserName")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
    url = 'http://127.0.0.1:8000/user/login'
    myobj = {'username': username ,'password': password }
    x_status = requests.post(url, data = myobj).status_code
    print(x_status)
    st.write(x_status)
    if x_status == 200:
        x = requests.post(url, data = myobj).json()    
        st.success("Login successful")
        log_username = x['username']
        log_token = x['access_token']
        print(log_username)
        print(log_token)
        st.write(x)
    elif x_status == 404 or x_status == 401:
        st.error("Login failed ... Invalid credentials")
    else:
        pass
    # st.write(requests.post("http://127.0.0.1:8000/user/login").json())
    # data = fetch(session, f"http://127.0.0.1:8000/user/login")
    # print(x)



