import streamlit as st
import pandas as pd
from datetime import datetime

# Speisekarte laden
speisekarte = pd.read_csv("Speisekarte.csv", 
                            sep=";", 
                            index_col="Speise_ID",
                            decimal=".")

# DataFrame für alle Bestellungen
bestellungen_df = pd.DataFrame(columns=[
                                "BestellID", 
                                "Datum", 
                                "Tischnummer", 
                                "SpeiseID", 
                                "Menge", 
                                "Status"]
                                )

# Funktion zur Erstellung einer neuen Bestellung
def neue_bestellung(tischnummer, speise_mengen, bestellungen_df, status="offen"):
    neue_bestellungen = []
    
    for speise_id, menge in speise_mengen.items():
        if not bestellungen_df.empty:
            bestellung_id = bestellungen_df.loc[bestellungen_df.index[-1], "BestellID"] + 1
        else:
            bestellung_id = 1
        datum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        neue_bestellungen.append([bestellung_id, 
                                datum, 
                                tischnummer, 
                                speise_id, 
                                menge, 
                                status])
    
    neue_bestellungen_df = pd.DataFrame(neue_bestellungen, 
                                        columns=bestellungen_df.columns)
    bestellungen_df = pd.concat([bestellungen_df, neue_bestellungen_df], ignore_index=True)
    
    return bestellungen_df

# STREAMLIT APP

def streamlit_app():
    """
    Definiert den Ablauf der App, sammelt die Eingaben und aktualisiert das DataFrame.
    
    """
    #global bestellungen_df

    # Leeres Dictionary zum Sammeln der Informationen
    # mit st.session_state wird jeder Zwischenstand gespeichert, 
    # sodass kein leeres Dictionary weiter gegeben wird
    if "speise_mengen" not in st.session_state:
        st.session_state.speise_mengen = {}
    
    # Initialisiere bestellungen_df im Session State
    if "bestellungen_df" not in st.session_state:
        st.session_state.bestellungen_df = pd.DataFrame(columns=[
            "BestellID", 
            "Datum", 
            "Tischnummer", 
            "SpeiseID", 
            "Menge", 
            "Status"])

    # Titel für Speisekarte
    st.title("Restaurant golden seagull")

    # Speisekarte anzeigen
    st.subheader("Speisekarte")
    st.dataframe(speisekarte)

    st.subheader("Bestellung aufgeben")

    # Tischnummer mit selectbox
    tischnummer = st.selectbox("Tischnummer", options=list(range(1, 16)), index=0)

    # Bestellstatus mit st.selectbox(bezahlt, offen, storno)
    bestellstatus = st.selectbox("Bestellstatus", options=["offen", "bezahlt", "storno"], index=0)
    
    # SpeiseID mit st.selectbox
    speise_id = st.selectbox("SpeiseID", options=[
        100, 101, 102, 103, 104, 105, 
        200, 201, 202, 203, 204, 205,
        300, 301, 302, 303, 304, 305, 
        400, 401, 402, 403, 404, 405, 406, 407, 408, 409], index=0)

    # Menge mit st.number_input
    menge = st.number_input("Menge", min_value=1, value=1)
    
    # Button:Erste Bedingung "Speise hinzufügen"
    # Ausgewählte SpeiseID wird gemeinsam mit Menge ins Dictionary "speise_mengen" eingefügt
    if st.button("Speise hinzufügen"):
        st.session_state.speise_mengen[speise_id] = menge
        st.write(f"Speise {speise_id} mit Menge {menge} hinzugefügt.")

    # Button:Zweite Bedingung "Bestellung aufgeben"
    # Überprüfung ob "speise_mengen" leer ist
    if st.button("Bestellung aufgeben"):
        if st.session_state.speise_mengen:
            st.session_state.bestellungen_df = neue_bestellung(
                tischnummer, 
                st.session_state.speise_mengen, 
                st.session_state.bestellungen_df, 
                bestellstatus)
            st.write("Bestellung erfolgreich aufgenommen!")
            # Leeren des dic: speise_mengen nach jeder Betellung
            st.session_state.speise_mengen = {}
        else:
            st.write("Bitte mindestens eine Speise hinzufügen.")
    
    st.subheader("Alle Bestellungen")
    st.dataframe(st.session_state.bestellungen_df)

if __name__ == "__main__":
    streamlit_app()


# Aktuell werden in das DataFrame bestellungen_df noch nicht alle Bestellungen gesammelt

# Ausführen des Skripts in Kommandozeile (Miniconda)
# cd "C:\Users\Admin\Git\Praxisprojekt-Python-Bestelltool"
# conda activate DataCraft
# streamlit run  "C:\Users\Admin\Git\Praxisprojekt-Python-Bestelltool\Bestelltool_streamlit.py"