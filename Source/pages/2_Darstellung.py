# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:30:05 2023

@author: Anna & Filipa
"""

import streamlit as st
import yaml, os
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import numpy as np
import pandas as pd
from Services import get_empty_data, convert_data_to_float
from jasonbin import load_key

st.set_page_config(page_title="Darstellung", page_icon="📈")

# -------- load secrets for jsonbin.io --------
jsonbin_secrets = st.secrets["jsonbin"]
api_key = jsonbin_secrets["api_key"]
bin_id = jsonbin_secrets["bin_id"]

# Loading config file (this file is in a sub folder!)
path = os.path.dirname(__file__)
head, tail = os.path.split(path)
CONFIGFILE = head+'/config.yaml'

with open(CONFIGFILE) as file:        
    config = yaml.load(file, Loader=SafeLoader)

#  Create the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# Render the login widget
fullname, authentication_status, username = authenticator.login('Login', 'main')

# Authenticate users
if authentication_status == True:   # login successful
    st.write(f'Welcome *{fullname}*')
    authenticator.logout('Logout', 'main')   # show logout button
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    if 'success' in st.session_state:
        del st.session_state['success']
    if 'data' in st.session_state:
        del st.session_state['data']
    st.stop()

st.markdown("""---""")
st.markdown("# 📈 Darstellung")
st.write(
    """
    Darstellung der erfassten Daten
    """
)

# Lokale Daten vorbereiten
if 'success' not in st.session_state:
    st.session_state.success = "Bereit..."

if 'data' not in st.session_state:
    # Daten einmalig via API Anfrage beziehen
    data = load_key(api_key, bin_id, username, get_empty_data())
    # Daten zwingend in float umwandeln
    st.session_state.data = convert_data_to_float(data)
    st.session_state.success = "Daten geladen!"
    
standards_list = st.session_state.data["standards"]
probes_list =  st.session_state.data["probes"]

# Sidebar aufbauen (Hilfe zur Bedienung)
st.sidebar.success(st.session_state.success)

# und in Datenframes überführen
df_std = pd.DataFrame(standards_list)
df_prb = pd.DataFrame(probes_list)

# X- und Y- Achse als Array extrahieren
x_std = df_std['Konzentration in mg/L'].to_numpy()
y_std = df_std['Extinktion'].to_numpy()

# Mit Numpy ein Lin-Fit machen (polyfit 1-Grades)
m,b = np.polyfit(x_std, y_std, 1)

# Chart zeichnen (leider kann streamlit keine Dots zeichnen, zumindest nicht nativ)
chart = st.line_chart(df_std, 
                      x = 'Konzentration in mg/L', 
                      y = 'Extinktion',
                      use_container_width = True)

# Neues Datenframe mit Steigung und Offset erzeugen
df_meta = pd.DataFrame()
df_meta["Steigung m"] = [m]
df_meta["Offset b"] = [b]
st.dataframe(df_meta, use_container_width = True)

x_prb = []
y_prb = df_prb['Extinktion'].to_numpy()
for y in y_prb:
    # Für Debug-Zwecke
    # st.write(str(y) + ' - ' + str(b) + ' / ' + str(m))
    x_prb.append((y-b)/m)

df_prb['Konzentration in mg/L'] = x_prb

# In zwei nebeneinander liegende Bereiche teilen
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Standards")
    st.dataframe(df_std,
                 use_container_width = True)
    
with col2:
    st.markdown("### Proben")
    st.dataframe(df_prb,
                 use_container_width = True)