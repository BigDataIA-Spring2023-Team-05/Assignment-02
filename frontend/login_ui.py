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
name = ['person1', 'person2']
uname = ['pp','cc']
psswd = ['123','321']
password = stauth.Hasher(psswd).generate()
## Converting above uname,name,passwd list into dictionary formation to use stauth:

credentials = {"usernames":{}}

for un, name, pw in zip(uname, name, password):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})


##

authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)
name , authentication_status , username = authenticator.login("Login","main")
if authentication_status == False:
    st.error("Username/Password  is incorrect")
    st.write(f"username : {username}")
if authentication_status == None:
    st.warning("Please enter your username and password")
    st.write(f"username : {username}")
if authentication_status == True:
    authenticator.logout("logout","main")


