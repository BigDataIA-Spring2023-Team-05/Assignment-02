## Library Imports
import pandas as pd
import numpy as mp
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
# name = ['person1', 'person2']
# uname = ['pp','cc']
# psswd = ['123','321']
# password = stauth.Hasher(psswd).generate()
# ## Converting above uname,name,passwd list into dictionary formation to use stauth:

# credentials = {"usernames":{}}

# for un, name, pw in zip(uname, name, password):
#     user_dict = {"name":name,"password":pw}
#     credentials["usernames"].update({un:user_dict})


##
import streamlit as st

# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your credentials")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit and email == actual_email and password == actual_password:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
    st.success("Login successful")
elif submit and email != actual_email or password != actual_password:
    st.error("Login failed")
else:
    pass




