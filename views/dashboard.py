import streamlit as st
import pandas as pd
import plotly.express as px
from views.efp_date_cloture import df_dates, closure_date

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Vous devez être connecté pour accéder à cette page.")
    st.stop()  # arrête l'exécution ici si pas connecté
    
# Check if data is available in session state
if 'df' in st.session_state:
    df = st.session_state.df
    
    # Fixer automatiquement selected_year en fonction de ce qui est présent dans fichier telecharge
    selected_year = 2024
    # Filter data for the year and Type Formation = 'Diplômante'
    year_data = df[(df['Année Scolaire'] == selected_year) & (df['Type Formation'] == 'Diplômante')]
    # Delete duplicates by Matricule Etudiant
    year_data = year_data.drop_duplicates(subset=['Matricule Etudiant'])
    # Convert 'Date PV' to datetime for filtering, handle errors if any value is invalid
    year_data['Date PV'] = pd.to_datetime(year_data['Date PV'], errors='coerce')
    year_data = year_data.dropna(subset=['Date PV'])
    # Clean the 'Etudiant Actif' column to remove extra spaces and handle case issues (Nettoyage des données qualitatives)
    year_data['Etudiant Actif'] = year_data['Etudiant Actif'].str.strip().str.lower()
#############################################################################################################
    efps = year_data['Code EFP'].dropna().unique()
    efp_results = []
    for efp in efps:
        efp_data = df[(df['Année Scolaire'] == selected_year) &
                   (df['Type Formation'] == 'Diplômante') &
                   (df['Code EFP'] == efp)]
        efp_data = efp_data.drop_duplicates(subset=['Matricule Etudiant'])
        total_efp_students = len(efp_data)
        # Nettoyer colonnes pour filtres
        efp_data['Date PV'] = pd.to_datetime(efp_data['Date PV'], errors='coerce')
        efp_data = efp_data.dropna(subset=['Date PV'])
        efp_data['Etudiant Actif'] = efp_data['Etudiant Actif'].str.strip().str.lower()
        # Filter out non-active students and those with registration after the closure date
        efp_dropout_data = efp_data[(efp_data['Type Formation'] == 'Diplômante')&
                                      (efp_data['Etudiant Actif'] == 'non') & 
                                      (efp_data['Date PV'] > pd.to_datetime(closure_date))]
        total_efp_non_active_students = len(efp_dropout_data)

        efp_reorientation_data = efp_data[(efp_data['Type Formation'] == 'Diplômante') &
                                            (efp_data['Etudiant Actif'] == 'non') & 
                                            (efp_data['Date PV'] > pd.to_datetime(closure_date)) & 
                                            (efp_data['Commentairesfs'].str.contains(r'(?i)\b(reo|réo|réorientation|reorientation)\b', regex=True, na=False))]
        total_efp_reorientation_students = len(efp_reorientation_data)

        total_efp_non_active_students = total_efp_non_active_students - total_efp_reorientation_students
        total_efp_active_students = total_efp_students - total_efp_non_active_students     

        dropout_efp_rate_1 = (total_efp_non_active_students / total_efp_students) * 100 if total_efp_students > 0 else 0
        dropout_efp_rate_2 = (total_efp_non_active_students / total_efp_active_students) * 100 if total_efp_active_students > 0 else 0
        dropout_efp_rate_percentage_1 = f"{dropout_efp_rate_1:.2f}%"
        dropout_efp_rate_percentage_2 = f"{dropout_efp_rate_2:.2f}%"
#############################################################################################################
        # Store the result for the efp
        efp_results.append({
            "Code EFP": efp,
            "Total des stagiaires diplômantes": total_efp_students,
            "Stagiaires diplômantes actifs": total_efp_active_students,
            "Stagiaires diplômantes déperdus": total_efp_non_active_students,
            "Taux de déperdition des inactifs par total": dropout_efp_rate_percentage_1,
            "Taux de déperdition des inactifs par actifs": dropout_efp_rate_percentage_2
            })
    # Convert the results to a DataFrame
    efp_df = pd.DataFrame(efp_results)
    # Merge efp_df with the df_dates
    merged_df = pd.merge(df_dates, efp_df, how="left", on="Code EFP")
    # Display the merged data in the dashboard
    st.write("### Tableau des établissements avec calculs associés")
    st.dataframe(merged_df)
#############################################################################################################
    efp_df['Taux de déperdition (%)'] = efp_df['Taux de déperdition des inactifs par actifs'].str.rstrip('%').astype(float) # Convertir la colonne en numérique
    fig_efp = px.bar(efp_df, 
                      x="Code EFP", 
                      y="Taux de déperdition (%)",
                      color="Code EFP", 
                      barmode="group", 
                      width=4000,
                      height=600,
                      title="📊 Taux de déperdition par établissement")
    fig_efp.update_traces(width=0.8)
    fig_efp.update_layout(xaxis_tickangle=-45,
                          margin=dict(l=40, r=40, t=80, b=150),
                          hovermode='x unified',
                          hoverdistance=100
                          )
    # Ordonner les barres pour avoir le plus grand taux en haut
    st.plotly_chart(fig_efp)  
#############################################################################################################
else:
    st.error("Aucune donnée disponible. Veuillez télécharger un fichier.")