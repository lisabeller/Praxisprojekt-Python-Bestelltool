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

# FUNKTION NEUE BESTELLUNG
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

# FUNKTION BESTELLUNG STORNIEREN
def bestellung_storno(bestellID, bestellungen_df = bestellungen_df):
    bestellungen_df.loc[bestellungen_df["BestellID"] == bestellID, "Status"] = "storno"  

    return bestellungen_df

# FUNKTION RECHNUNG ERSTELLEN
def brutto_nettorechner(bruttopreis, stueckzahl, mwst=0.19):
    gesamt_bruttopreis = bruttopreis * stueckzahl
    nettopreis = gesamt_bruttopreis / (1 + mwst)
    steuerbetrag = gesamt_bruttopreis - nettopreis

    return gesamt_bruttopreis, nettopreis, steuerbetrag

def bestellung_bezahlen(bestellID, bestellungen_df = bestellungen_df, speisekarte=speisekarte):
    # Status auf "bezahlt" setzten
    bestellungen_df.loc[bestellungen_df["BestellID"] == bestellID, "Status"] = "bezahlt"

    # Filtert die Bestellungen nach der BestellID
    bestellung_details = bestellungen_df[bestellungen_df["BestellID"] == bestellID]
    
    # Funktion für DataFrame der Rechnung
    def berechne_rechnung(row):
        
        # Variablen
        speise_id = row["SpeiseID"]
        menge = row["Menge"]
        bruttopreis = speisekarte.loc[speise_id, "Preis"]

        # Datum ohne Uhrzeit formatieren
        datum = datetime.strptime(row["Datum"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

        # Errechnet Netto und Steuerbetrag
        gesamt_brutto, netto, steuer = brutto_nettorechner(bruttopreis, menge)

        return pd.Series({
            "BestellID": row["BestellID"],
            "Datum": datum,
            "Tischnr": row["Tischnummer"],
            "SpeiseID": speise_id,
            "Menge": menge,
            "Nettopreis": round(netto, 2),
            "Steuer(19%)": round(steuer, 2),
            "Bruttopreis": round(gesamt_brutto, 2),
        })
    # Berechnet die Rechnung für jede Zeile in bestellung_details
    rechnung_df = bestellung_details.apply(berechne_rechnung, axis=1)

    # Gesamtbetrag in neue Zeile einfügen
    letzte_zeile = rechnung_df.iloc[-1]

    neue_zeile_df = pd.DataFrame({
                    "BestellID": ["Gesamt"],
                    "Datum": [""],
                    "Tischnr": [""],
                    "SpeiseID": [""],
                    "Menge": [rechnung_df["Menge"].sum()],
                    "Nettopreis": [rechnung_df["Nettopreis"].sum()],
                    "Steuer(19%)": [rechnung_df["Steuer(19%)"].sum()],
                    "Bruttopreis": [rechnung_df["Bruttopreis"].sum()]
                    })

    rechnung_df = pd.concat([rechnung_df, neue_zeile_df], ignore_index=True)
    
    return rechnung_df


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
    
    st.subheader("Bestellung stornieren")

    vorhandene_bestellIDs = st.session_state.bestellungen_df["BestellID"].unique().tolist()
    ausgewählte_bestellID = st.selectbox("BestellID", options=vorhandene_bestellIDs)

    # Auswahl der BestellID über Dropdown
    if st.button("Bestellung stornieren"):
        if ausgewählte_bestellID:
            st.session_state.bestellungen_df = bestellung_storno(ausgewählte_bestellID, 
                                                st.session_state.bestellungen_df)
            st.write(f"Bestellung {ausgewählte_bestellID} wurde storniert.")
        else:
            st.write("Bitte eine gültige BestellID auswählen.")

    st.subheader("Rechnung erstellen")
    # Auswahl der BestellID über Dropdown
    if st.button("Rechnung anzeigen"):
        if ausgewählte_bestellID:
            rechnung_df = bestellung_bezahlen(ausgewählte_bestellID, st.session_state.bestellungen_df, speisekarte)
            st.write("Rechnung für BestellID: ", ausgewählte_bestellID)
            st.dataframe(rechnung_df)
        else:
            st.write("Bitte eine gültige BestellID auswählen.")

if __name__ == "__main__":
    streamlit_app()



# Ausführen des Skripts in Kommandozeile (Miniconda)
# cd "C:\Users\Admin\Git\Praxisprojekt-Python-Bestelltool"
# conda activate DataCraft
# streamlit run  "C:\Users\Admin\Git\Praxisprojekt-Python-Bestelltool\Bestelltool_streamlit.py"