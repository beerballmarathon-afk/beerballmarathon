import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURAZIONE LINK (MODIFICA SOLO QUI) ---
# Incolla qui i link CSV di Google Sheets
URL_CALENDARIO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_prRD0nsNLmgShBA-n-QqnmCbcYWRvEZ_MYpS9DpARhj43CCbGjcR7EdCb9YlEsqNQsePKZY5YtE/pub?gid=1738657109&single=true&output=csv"
URL_TEAM = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_prRD0nsNLmgShBA-n-QqnmCbcYWRvEZ_MYpS9DpARhj43CCbGjcR7EdCb9YlEsqNQsePKZY5YtE/pub?gid=1955830524&single=true&output=csv"
URL_BEERCUP = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_prRD0nsNLmgShBA-n-QqnmCbcYWRvEZ_MYpS9DpARhj43CCbGjcR7EdCb9YlEsqNQsePKZY5YtE/pub?gid=1684440180&single=true&output=csv"

# Incolla qui i link ai tuoi PDF su Google Drive (assicurati che siano pubblici)
LINK_REGOLAMENTO = "https://docs.google.com/document/d/e/2PACX-1vSItQqV4_poywuIiJLu9hzQdjRlU5u1aXYGUVr5LVH7FtFER88T4poFJxPqY40Tx81OTJD_bCm9P4Xd/pub"
LINK_ISCRIZIONE = "https://docs.google.com/document/d/e/2PACX-1vT5_-P8WNOmRry8CUeQZLj9jh5U_ogR_2SLOeZiJoiUTicQaAdlyTPmfNtJO4y1ng/pub"
LINK_FOTO = "https://link_alle_tue_foto.com"

# --- 2. IMPOSTAZIONI PAGINA ---
st.set_page_config(page_title="Green Volley Hub", page_icon="🏐", layout="wide")
st_autorefresh(interval=60000, key="datarefresh")

# Funzione per caricare i dati
def load_data(url):
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# Gestione della navigazione (Stato della pagina)
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

def nav(page_name):
    st.session_state.page = page_name

# --- 3. BARRA LATERALE ---
st.sidebar.title("🏐 Menu Rapido")
if st.sidebar.button("🏠 Torna alla Home"):
    nav("🏠 Home")
st.sidebar.write("---")
st.sidebar.info("I dati si aggiornano automaticamente ogni minuto.")

# --- 4. LOGICA DELLE PAGINE ---

# --- HOME PAGE ---
if st.session_state.page == "🏠 Home":
    st.title("🏐 Torneo Green Volley 2026")
    st.subheader("Dashboard Principale")
    
    # Griglia di bottoni per la navigazione
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅 CALENDARIO & RISULTATI", use_container_width=True): nav("📅 Calendario")
        if st.button("🏆 CLASSIFICHE GIRONI", use_container_width=True): nav("🏆 Classifiche")
        if st.button("🍺 BEER CUP", use_container_width=True): nav("🍺 Beer Cup")
    with col2:
        if st.button("🏅 FASE FINALE (Gold/Silver)", use_container_width=True): nav("🏅 Fase Finale")
        if st.button("🛒 SHOP & SCONTI", use_container_width=True): nav("🛒 Shop")
        if st.button("📸 GALLERY FOTO", use_container_width=True): nav("📸 Foto")

    st.write("---")
    st.subheader("📄 Documenti Utili")
    d1, d2 = st.columns(2)
    with d1:
        st.link_button("📜 Leggi Regolamento (PDF)", LINK_REGOLAMENTO, use_container_width=True)
    with d2:
        st.link_button("📝 Scarica Modulo Iscrizione (PDF)", LINK_ISCRIZIONE, use_container_width=True)

# --- CALENDARIO ---
elif st.session_state.page == "📅 Calendario":
    st.header("📅 Calendario e Risultati Live")
    df = load_data(URL_CALENDARIO)
    if not df.empty:
        gironi = ["Tutti"] + sorted(list(df['Girone'].unique()))
        filtro = st.selectbox("Seleziona il tuo Girone:", gironi)
        df_show = df if filtro == "Tutti" else df[df['Girone'] == filtro]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
    else:
        st.error("Dati del calendario non trovati.")

# --- CLASSIFICHE ---
elif st.session_state.page == "🏆 Classifiche":
    st.header("🏆 Classifica Gironi")
    st.info("Le prime 2 squadre di ogni girone accedono al torneo GOLD. 3ª e 4ª al SILVER.")
    df_cal = load_data(URL_CALENDARIO)
    if not df_cal.empty:
        # Calcolo punti semplificato (3 pt vittoria)
        punti = {}
        for _, r in df_cal[df_cal['Stato'] == 'Finito'].iterrows():
            sA, sB, vA, vB = r['Squadra A'], r['Squadra B'], int(r['Set A']), int(r['Set B'])
            punti[sA] = punti.get(sA, 0) + (3 if vA > vB else 0)
            punti[sB] = punti.get(sB, 0) + (3 if vB > vA else 0)
        
        classifica_df = pd.DataFrame(list(punti.items()), columns=['Squadra', 'Punti']).sort_values(by='Punti', ascending=False)
        st.table(classifica_df)
    else:
        st.warning("In attesa dei primi risultati...")

# --- FASE FINALE ---
elif st.session_state.page == "🏅 Fase Finale":
    st.header("🏅 Fase Finale")
    gold, silver = st.tabs(["🔥 TORNEO GOLD", "🛡️ TORNEO SILVER"])
    with gold:
        st.subheader("Tabellone ad eliminazione diretta - GOLD")
        st.write("Incroci: 1ª Girone A vs 2ª Girone B | 1ª Girone B vs 2ª Girone A... ecc.")
        # Qui potrai inserire una tabella o un'immagine del tabellone
    with silver:
        st.subheader("Tabellone ad eliminazione diretta - SILVER")

# --- BEER CUP ---
elif st.session_state.page == "🍺 Beer Cup":
    st.header("🍺 Classifica Beer Cup")
    df_beer = load_data(URL_BEERCUP)
    if not df_beer.empty:
        st.bar_chart(df_beer.set_index("Squadra"))
        st.table(df_beer.sort_values(by="Consumazioni", ascending=False))

# --- SHOP ---
elif st.session_state.page == "🛒 Shop":
    st.header("🛒 Shop & Area Sconti")
    df_team = load_data(URL_TEAM)
    with st.expander("Login Squadra per Sconti"):
        user = st.text_input("Nome Squadra")
        pw = st.text_input("Password", type="password")
        if st.button("Verifica"):
            if any((df_team['Nome Squadra'] == user) & (df_team['Password'].astype(str) == pw)):
                st.success(f"Log-in riuscito! Codice Sconto Bar: GREEN-SHT-20")
            else:
                st.error("Dati non corretti.")

# --- FOTO ---
elif st.session_state.page == "📸 Foto":
    st.header("📸 Gallery")
    st.write("Guarda le foto ufficiali della giornata.")
    st.link_button("Apri Album Foto", LINK_FOTO)