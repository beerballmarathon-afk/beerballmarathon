import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Green Volley Hub", page_icon="🏐", layout="wide")

# Aggiornamento automatico ogni 60 secondi
st_autorefresh(interval=60000, key="datarefresh")

# INSERISCI QUI I TUOI LINK CSV DI GOOGLE SHEETS
URL_CALENDARIO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_prRD0nsNLmgShBA-n-QqnmCbcYWRvEZ_MYpS9DpARhj43CCbGjcR7EdCb9YlEsqNQsePKZY5YtE/pub?gid=1738657109&single=true&output=csv"
URL_TEAM = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_prRD0nsNLmgShBA-n-QqnmCbcYWRvEZ_MYpS9DpARhj43CCbGjcR7EdCb9YlEsqNQsePKZY5YtE/pub?gid=1955830524&single=true&output=csv"
URL_BEERCUP = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_prRD0nsNLmgShBA-n-QqnmCbcYWRvEZ_MYpS9DpARhj43CCbGjcR7EdCb9YlEsqNQsePKZY5YtE/pub?gid=1684440180&single=true&output=csv"

# Funzione caricamento dati
def load_data(url):
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# --- SIDEBAR ---
st.sidebar.title("BBM 2026")
menu = ["Home 🏠", "Calendario 📅", "Classifica 🏆", "BeerBall Cup 🍺", "Shop & Sconti 🛒", "Foto 📸", ]
choice = st.sidebar.radio("Menu", menu)

# --- LOGICA PAGINE ---

if choice == "Home 🏠":
    st.header("Benvenuti al BeerBall Marathon 2026")
    st.write("Qui trovi tutte le informazioni ufficiali, i risultati live e la classifica del tuo girone.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📜 Regolamento")
        st.info("Partite ai 2 set su 3 (al 21). Terzo set eventuale al 15. Cambio campo ogni 7 punti.")
    with col2:
        st.subheader("📝 Iscrizioni")
        st.write("I moduli devono essere consegnati entro le 08:30 al desk.")

elif choice == "Calendario 📅":
    st.header("📅 Calendario Partite")
    df_cal = load_data(URL_CALENDARIO)
    
    if not df_cal.empty:
        gironi = ["Tutti"] + list(df_cal['Girone'].unique())
        filtro_g = st.selectbox("Filtra per Girone", gironi)
        
        df_display = df_cal if filtro_g == "Tutti" else df_cal[df_cal['Girone'] == filtro_g]
        
        # Formattazione estetica
        st.dataframe(df_display.style.highlight_max(axis=0, subset=['Stato']), use_container_width=True)
    else:
        st.warning("Carica i dati nel foglio Calendario!")

elif choice == "Classifica 🏆":
    st.header("🏆 Classifica Sportiva")
    df_cal = load_data(URL_CALENDARIO)
    
    if not df_cal.empty:
        # Logica punti semplificata: 3 punti vittoria, 1 punto pareggio (se previsto)
        punti = {}
        for _, row in df_cal[df_cal['Stato'] == 'Finito'].iterrows():
            sA, sB = row['Squadra A'], row['Squadra B']
            setA, setB = int(row['Set A']), int(row['Set B'])
            
            punti[sA] = punti.get(sA, 0) + (3 if setA > setB else 0)
            punti[sB] = punti.get(sB, 0) + (3 if setB > setA else 0)
        
        res_classifica = pd.DataFrame(list(punti.items()), columns=['Squadra', 'Punti']).sort_values(by='Punti', ascending=False)
        st.table(res_classifica)
    else:
        st.write("Nessun risultato ancora inserito.")

elif choice == "🍺 Beer Cup":
    st.header("🍺 Classifica Beer Cup")
    st.write("Chi sta vincendo la sfida al bar?")
    df_beer = load_data(URL_BEERCUP)
    if not df_beer.empty:
        df_beer = df_beer.sort_values(by="Consumazioni", ascending=False)
        st.bar_chart(data=df_beer, x="Squadra", y="Consumazioni", color="#FFA500")
        st.table(df_beer)

elif choice == "🛒 Shop & Sconti":
    st.header("🛒 Area Riservata Squadre")
    df_team = load_data(URL_TEAM)
    
    with st.form("login"):
        user = st.text_input("Nome Squadra")
        pwd = st.text_input("Password", type="password")
        submit = st.form_submit_button("Accedi")
        
    if submit:
        if any((df_team['Nome Squadra'] == user) & (df_team['Password'].astype(str) == pwd)):
            st.success(f"Log-in effettuato! Ciao {user}")
            st.balloons()
            st.info("🎟️ COUPON BAR: Mostra questo codice per 1 giro di shot omaggio: **SHOT-GREEN**")
            
            st.write("---")
            st.subheader("👕 Pre-order Merchandising")
            st.selectbox("Articolo", ["Maglia Torneo 2026", "Cappellino Pro", "Sacca Green Volley"])
            st.number_input("Quantità", min_value=1)
            st.button("Invia Pre-ordine")
        else:
            st.error("Dati errati. Riprova o chiedi al desk.")

elif choice == "📸 Foto":
    st.header("📸 Foto del Torneo")
    st.write("Le foto verranno caricate a fine giornata!")
    st.link_button("Apri Album Google Foto", "https://photos.google.com")
