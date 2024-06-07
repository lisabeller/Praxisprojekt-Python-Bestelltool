## Projektbeschreibung
Das Restaurant “golden seagull” benötigt ein Programm zur Abwicklung von Bestellungen im
Restaurant und beauftragt euch als selbstständiges, kleines Developer-Team mit der Entwicklung
der Software. 

## Erläuterung des Codes

#### Allgemeines
Frameworks und Bibliotheken: Der Code nutzt Streamlit zur Erstellung einer Web-App, pandas zur Datenverarbeitung, datetime für Datumsoperationen und PIL zur Bildverarbeitung.
Daten laden und initialisieren
Speisekarte laden: Eine CSV-Datei Speisekarte.csv wird in ein DataFrame geladen, das die Gerichte und deren Preise enthält.
Bestellungen DataFrame: Ein leeres DataFrame für alle Bestellungen wird initialisiert mit den Spalten "BestellID", "Datum", "Tischnummer", "SpeiseID", "Menge", und "Status".
#### Funktionen
Neue Bestellung: neue_bestellung fügt neue Bestellungen hinzu, indem es eine eindeutige BestellID generiert und die Bestelldaten in das DataFrame einfügt.
Bestellung stornieren: bestellung_storno setzt den Status einer Bestellung auf "storno".
Rechnung erstellen: bestellung_bezahlen setzt den Status einer Bestellung auf "bezahlt", berechnet die Nettopreise und die Mehrwertsteuer und erstellt ein DataFrame für die Rechnung.
Bestellungen speichern: bestellungen_speichern speichert das Bestellungen-DataFrame als CSV-Datei.
#### Streamlit App
App-Titel und Bild: Der Titel "Restaurant Bestelltool" wird angezeigt und ein Bild der Speisekarte geladen.
Bestellung aufgeben: Benutzer können eine Tischnummer, Bestellstatus, SpeiseID und Menge auswählen, um eine Bestellung aufzugeben.
Bestellungen anzeigen: Eine Übersicht aller Bestellungen wird angezeigt.
Bestellung stornieren: Benutzer können eine BestellID auswählen, um eine Bestellung zu stornieren.
Rechnung erstellen: Benutzer können eine BestellID auswählen, um eine Rechnung anzuzeigen.
Bestellungen speichern: Ein Button, um die aktuelle Bestellliste als CSV-Datei zu speichern.
#### Besondere Hinweise
Session State: Nutzung von st.session_state zur Speicherung von Bestellungen und Speisenmengen, um die Daten zwischen den Interaktionen zu behalten.
UI-Elemente: Verschiedene Streamlit-Widgets wie selectbox, number_input, button und dataframe zur Interaktion mit dem Benutzer.

#### Verwendung des Codes
# Ausführen des Skripts über Kommandozeile (z.B.Miniconda)
# streamlit run  "Dateipfad"
