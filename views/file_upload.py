import pandas as pd
import streamlit as st

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Vous devez être connecté pour accéder à cette page.")
    st.stop()  # arrête l'exécution ici si pas connecté

# File upload section
uploaded_file = st.file_uploader("📂 Choisissez un fichier Excel...", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # Check if required columns are present
    if 'Année Scolaire' not in df.columns or 'Etudiant Actif' not in df.columns or 'Date PV' not in df.columns or 'Type Formation' not in df.columns:
        st.error("Le fichier ne contient pas toutes les colonnes nécessaires.")
    else:
        st.success("Fichier valide !")
        st.session_state.df = df  # Store the dataframe in session state for later use
