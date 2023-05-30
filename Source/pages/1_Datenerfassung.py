# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:30:05 2023

@author: Anna & Filipa
"""

import streamlit as st
import yaml, os
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from Services import get_empty_data, convert_data_to_float
from jasonbin import load_key, save_key

# Seite darstellen
st.set_page_config(page_title="Datenerfassung", page_icon="📊")

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
st.markdown("# 📊 Datenerfassung")
st.write(
    """
    Auf dieser Seite können die Daten erfasst werden.
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
st.sidebar.title("Bedienung beim Bearbeiten")
st.sidebar.header("Hinzufügen")
st.sidebar.markdown("Plus auf der letzten Zeile klicken")
st.sidebar.header("Ändern")
st.sidebar.markdown("Zeile markieren und Werte anpassen")
st.sidebar.header("Entfernen")
st.sidebar.markdown("Eine oder mehrere Zeilen markieren und Taste *del* drücken")

# Success auf default zurücksetzen 
st.session_state.success = "Bereit..."

# Weiter mit Seiteninhalt...
function_radio = st.radio("Funktion", 
                          ('Anzeigen', 'Bearbeiten'), 
                          label_visibility='hidden',
                          horizontal=True)
# Leere Zeile
st.write("")

# In zwei nebeneinander liegende Bereiche teilen
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Standards")
with col2:
    st.markdown("### Proben")

if function_radio == 'Anzeigen':
    with col1:
        standards_list = st.dataframe(data = standards_list, 
                                      use_container_width = True)
    
    with col2:
        probes_list = st.dataframe(data = probes_list, 
                                   use_container_width = True)
else:
    with col1:
        standards_list_edit = st.experimental_data_editor(data = standards_list, 
                                                          use_container_width = True,
                                                          num_rows="dynamic")

    with col2:
        probes_list_edit = st.experimental_data_editor(data = probes_list, 
                                                       use_container_width = True,
                                                       num_rows="dynamic")

    save_button = st.button("💾 Daten speichern")
    
    if save_button == True:         
        data = {
            "standards": standards_list_edit, 
            "probes":  probes_list_edit
        }
        
        st.session_state.data = data
        
        res = save_key(api_key, bin_id, username, data)
        if 'message' in res:
            st.error('Fehler beim Speichern der Daten!', icon="🚨")
        else:
            st.success('Daten erfolgreich gespeichert!', icon="✅")