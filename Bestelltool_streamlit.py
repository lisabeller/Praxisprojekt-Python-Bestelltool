import streamlit as st
from datetime import datetime

# Titel für die Webanwendung
st.title("Speisekarte anzeigen")

# Speisekarte anzeigen

# BESTELLUNG
# Tischnummer mit selectbox
# SpeiseID mit st.selectbox
# Menge mit st.number_input
# Bestellstatus mit st.radio(bezahlt, offen)
# Button für weitere Bestellung(Funktion hinterlegen)


st.radio("Beschreibung", ("JA", "NEIN"))


# Ausführen des Skripts mit `streamlit run "Pfad"` in Kommandozeile (Miniconda)