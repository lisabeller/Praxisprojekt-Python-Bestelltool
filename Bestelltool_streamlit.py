import streamlit as st
from datetime import datetime

# Titel für die Webanwendung
st.title()

st.selectbox(["LISTE"])

st.radio("Beschreibung", ("JA", "NEIN"))

st.number_input(min_value=1800, max_value=datetime.now().year, format='%d')


# Ausführen des Skripts mit `streamlit run "Pfad"` in Kommandozeile (Miniconda)