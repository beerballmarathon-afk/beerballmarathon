import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Green Volley Hub", page_icon="🏐", layout="wide")
st_autorefresh(interval=60000, key="datarefresh")

# --- LINK DATABASE (Inserisci i tuoi link CSV qui) ---
URL_CALENDARIO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_prRD0nsNLmgShBA-n-QqnmCbcYWRvEZ_MYpS9DpARhj43CCbGjcR7EdCb9YlEsqNQsePKZY5YtE/pub?gid=1738657109&single=true&output=csv"
URL_TEAM = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_prRD0nsNLmgShBA-n-QqnmCbcYWRvEZ_MYpS9DpARhj43CCbGjcR7EdCb9YlEsqNQsePKZY5YtE/pub?gid=1955830524&single=true&output=csv"
URL_BEERCUP = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_prRD0nsNLmgShBA-n-QqnmCbcYWRvEZ_MYpS9DpARhj43CCbGjcR7EdCb9YlEsqNQsePKZY5YtE/pub?gid=1684440180&single=true&output=csv"

def load_data(url):
    try: return pd.read_csv(url)
    except: return pd.DataFrame()

# --- LOGICA NAVIGAZIONE ---
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

def set_page(name):
    st.session_state.page = name

# --- SIDEBAR ---
st.sidebar.title("🏐 Menu Torneo")
if st.sidebar.button("🏠 Torna alla Home"):
    set_page("🏠 Home")

# --- PAGINE ---

if st.session_state.page == "🏠 Home":
    st.title("🏐 Green Volley 2026")
    st.subheader("Benvenuti! Seleziona una sezione:")
    
    # DASHBOARD A BOTTONI (Griglia 2x2 o 3x2)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅 CALENDARIO & RISULTATI", use_container_width=True): set_page("📅 Calendario")
        if st.button("🏆 CLASSIFICHE GIRONI", use_container_width=True): set_page("🏆 Classifiche")
        if st.button("🍺 BEER CUP (Live)", use_container_width=True): set_page("🍺 Beer Cup")
    with col2:
        if st.button("🏅 FASE FINALE (Gold/Silver)", use_container_width=True): set_page("🏅 Fase Finale")
        if st.button("🛒 SHOP & SCONTI", use_container_width=True): set_page("🛒 Shop")
        if st.button("📸 GALLERY FOTO", use_container_width=True): set_page("📸 Foto")

    st.write("---")
    # SEZIONE DOCUMENTI PDF
    st.subheader("📄 Documenti e Regolamenti")
    c1, c2 = st.columns(2)
    with c1:
        # Esempio Link a Google Drive
        st.link_button("📜 Leggi Regolamento (PDF)", "URL_DEL_TUO_PDF_SU_GOOGLE_DRIVE", use_container_width=True)
    with c2:
        st.link_button("📝 Modulo Iscrizione (PDF)", "URL_DEL_TUO_MODULO_SU_GOOGLE_DRIVE", use_container_width=True)

elif st.session_state.page == "📅 Calendario":
    st.header("📅 Calendario Partite")
    if st.button("⬅️ Torna alla Home"): set_page("🏠 Home")
    # ... (Codice calendario precedente) ...

elif st.session_state.page == "🏆 Classifiche":
    st.header("🏆 Classifiche Gironi")
    if st.button("⬅️ Torna alla Home"): set_page("🏠 Home")
    # Qui il sistema calcola chi è 1°, 2°, 3°, 4°
    st.info("Le prime 2 passano al GOLD, 3° e 4° al SILVER.")
    # ... (Logica calcolo punti) ...

elif st.session_state.page == "🏅 Fase Finale":
    st.header("🏅 Fase Finale")
    if st.button("⬅️ Torna alla Home"): set_page("🏠 Home")
    
    tab1, tab2 = st.tabs(["🔥 TORNEO GOLD (1°-2°)", "❄️ TORNEO SILVER (3°-4°)"])
    
    with tab1:
        st.subheader("Tabellone GOLD")
        st.write("Quarti di Finale | Semifinali | Finale")
        # Qui potrai inserire un'immagine del tabellone o una tabella dedicata
        st.image("https://via.placeholder.com/800x400.png?text=Tabellone+Gold+In+Arrivo")

    with tab2:
        st.subheader("Tabellone SILVER")
        st.image("https://via.placeholder.com/800x400.png?text=Tabellone+Silver+In+Arrivo")

elif st.session_state.page == "🍺 Beer Cup":
    st.header("🍺 Beer Cup")
    if st.button("⬅️ Torna alla Home"): set_page("🏠 Home")
    # ... (Codice Beer Cup precedente) ...

# (E così via per le altre pagine...)


