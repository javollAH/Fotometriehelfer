# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 11:07:53 2023

@author: Anna & Filipa
"""

import streamlit as st

st.set_page_config(
    page_title="Fotometrie-Helfer",
    page_icon="👋",
)

st.write("# 👋 Fotometrie-Helfer!")

st.sidebar.success("Bereit...")

st.markdown(
    """
    ## Fotometrie — das Wichtigste
    - Die Photometrie ist ein Messverfahren zur Konzentrationsbestimmung von gelösten Substanzen durch Messung ihrer Transmission.
    - Über Messung der Transmission kann die Extinktion bestimmt werden.
    - Die Extinktion umfasst die folgenden lichtschwächenden Prozesse: Absorption, Reflexion und Brechung.
    - Das Messgerät zur photometrischen Messung ist ein Photometer. 
    - Die Eigenschaften des Photometers sind der geringe Zeitaufwand und seine hohe Präzision.
    
    👈 Bitte in der Sidebar Dateneingabe oder Datendarstellung wählen!

    ### Willst du mehr über Fotometrie wissen?
    - Check out [studyflix.de](https://studyflix.de/chemie/photometrie-5394)
    - Check out [wikipedia.org](https://de.wikipedia.org/wiki/Photometrie) 

    ### Diese App wurde mit streamlit ermöglicht
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
"""
)