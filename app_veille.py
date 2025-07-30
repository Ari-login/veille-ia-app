import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Connexion à Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Charger la feuille
sheet = client.open_by_key("1KdVDD9fD6kDu6Y1Lqja3yuJyHZiSlWUENAHfexbxY8k")  # Remplace par ton ID
worksheet = sheet.worksheet("Veille_IA")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Format de la date
df['Date'] = pd.to_datetime(df['Date'])

# Interface Streamlit
st.set_page_config(page_title="Veille IA / Big Data", layout="wide")
st.title("🧠 Veille IA & Big Data – SAH Analytics")

# Filtres
st.sidebar.header("🔎 Filtres")
sources = st.sidebar.multiselect("Filtrer par source", df['Source'].unique(), default=list(df['Source'].unique()))
mots = st.sidebar.text_input("Contient le mot (optionnel)", "")

filtre = df[df['Source'].isin(sources)]
if mots:
    filtre = filtre[filtre['Titre'].str.contains(mots, case=False)]

# KPIs
st.metric("📄 Articles récents", len(filtre))
st.metric("🗓️ Semaine en cours", len(filtre[filtre["Date"] >= pd.Timestamp.now().normalize() - pd.Timedelta(days=7)]))

# Tableau
st.subheader("📋 Liste des articles")
for _, row in filtre.sort_values(by='Date', ascending=False).iterrows():
    st.markdown(f"""
    **📰 {row['Titre']}**  
    🕒 {row['Date'].strftime('%Y-%m-%d')} | 🏷️ {row['Source']}  
    🔗 [Lire l'article]({row['Lien']})  
    ---
    """)

