import streamlit as st
import pandas as pd
from pathlib import Path

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Vous devez être connecté pour accéder à cette page.")
    st.stop()  # arrête l'exécution ici si pas connecté

st.title("Gestion de la Date de Clôture par Établissement")

DATE_FILE_PATH = Path("data/efp_date_cloture.xlsx")
# Charger les données du fichier Excel
try:
    df_dates = pd.read_excel(DATE_FILE_PATH)
except FileNotFoundError:
    st.error(f"Le fichier est introuvable.")
    st.stop()

# Vérifier les colonnes indispensables
required_cols = ['EFP', 'Code EFP', 'Date Clôture']
if not all(col in df_dates.columns for col in required_cols):
    st.error(f"Le fichier doit contenir les colonnes : {required_cols}")
    st.stop()

col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
with col1:
    selected_efp = st.selectbox("🏢 Choisissez un établissement", df_dates['EFP'].unique())
    current_date = df_dates.loc[df_dates['EFP'] == selected_efp, 'Date Clôture'].values[0]
    # Formater la date actuelle avant l'affichage
    current_date_formatted = pd.to_datetime(current_date).strftime('%d/%m/%Y')  # format souhaité
with col2:
    new_date = st.date_input("🗓️ Date de clôture", pd.to_datetime(current_date))

# Bouton de mise à jour
if st.button("💾 Mettre à jour la date de clôture"):
    df_dates.loc[df_dates['EFP'] == selected_efp, 'Date Clôture'] = new_date.strftime('%d/%m/%Y')
    df_dates.to_excel(DATE_FILE_PATH, index=False)
    st.success(f"Date de clôture mise à jour avec succès.")
closure_date = pd.to_datetime(new_date)
st.write("### Liste des établissements")
st.dataframe(df_dates[['EFP', 'Code EFP', 'Date Clôture']])