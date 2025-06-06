import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(page_title="Statistics Dashboard", page_icon=":bar_chart:", layout="wide")

# Check if data is available in session state
if 'df' in st.session_state:
    df = st.session_state.df

    # Choose year and closure date
    years_available = df['Année Scolaire'].dropna().unique()
    # Ensure the 'Année Scolaire' values are treated as strings or integers for sorting
    years_available = sorted(years_available, key=lambda x: str(x))
#############################################################################################################
    col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
    with col1:
        selected_year = st.selectbox("📅 Choisissez l'année scolaire", years_available)
    with col2:
        closure_date = st.date_input("🗓️ Choisissez la date de clôture", value=datetime.date(2024, 10, 31))
#############################################################################################################
    st.title("Affichage des calcules")

    # Filter data for the selected year and Type Formation = 'Diplômante'
    year_data = df[(df['Année Scolaire'] == selected_year) & (df['Type Formation'] == 'Diplômante')]
    # Delete duplicates by Matricule Etudiant
    year_data = year_data.drop_duplicates(subset=['Matricule Etudiant'])
    # Calculate total students
    total_students = len(year_data)

    # Convert 'Date PV' to datetime for filtering, handle errors if any value is invalid
    year_data['Date PV'] = pd.to_datetime(year_data['Date PV'], errors='coerce')
    year_data = year_data.dropna(subset=['Date PV'])
    # Clean the 'Etudiant Actif' column to remove extra spaces and handle case issues
    year_data['Etudiant Actif'] = year_data['Etudiant Actif'].str.strip().str.lower()

    # Filter out non-active students and those with registration after the closure date
    dropout_data = year_data[(year_data['Type Formation'] == 'Diplômante')&
                             (year_data['Etudiant Actif'] == 'non') & 
                              (year_data['Date PV'] > pd.to_datetime(closure_date))]

    # Calculate total number of students and non-active students
    total_non_active_students = len(dropout_data)

    # Filter students who have 'reorientation' in 'Commentairesfs'
    reorientation_data = year_data[(year_data['Type Formation'] == 'Diplômante') &
                                   (year_data['Etudiant Actif'] == 'non') & 
                                   (year_data['Date PV'] > pd.to_datetime(closure_date)) & 
                                    (year_data['Commentairesfs'].str.contains(r'(?i)\b(reo|réo|réorientation|reorientation)\b', regex=True, na=False))]

    # Calculate total non-active students with 'reorientation'
    total_reorientation_students = len(reorientation_data)

    # Subtract the reorientation students from the total non-active students
    total_non_active_students = total_non_active_students - total_reorientation_students

    #Calculate the total number of active students
    total_active_students = total_students - total_non_active_students

    # Calculate dropout rate based on total students
    dropout_rate_1 = (total_non_active_students / total_students) * 100 if total_students > 0 else 0
    dropout_rate_percentage_1 = f"{dropout_rate_1:.2f}%"

    # Calculate dropout rate based on active students
    dropout_rate_2 = (total_non_active_students / total_active_students) * 100 if total_active_students > 0 else 0
    dropout_rate_percentage_2 = f"{dropout_rate_2:.2f}%"
#############################################################################################################
    # Display total students, non-active students, and dropout rate
    st.write(f"📉 Total des stagiaires diplômantes pour l'année {selected_year}: {total_students}")
    st.write(f"📉 Total des stagiaires diplômantes actifs: {total_active_students}")
    st.write(f"📉 Total des stagiaires diplômantes déperdus: {total_non_active_students}")
    st.write(f"🔴 Taux de déperdition pour l'année {selected_year} des inactifs par actifs : {dropout_rate_percentage_2}")
    st.write(f"🔴 Taux de déperdition pour l'année {selected_year} des inactifs par total : {dropout_rate_percentage_1}")
#############################################################################################################
    st.title("Affichage de taux de déperdition par chaque parametres")
#############################################################################################################
    departments = year_data['Dept'].dropna().unique()
    department_results = []

    for dept in departments:
        dept_data = df[(df['Année Scolaire'] == selected_year) &
                   (df['Type Formation'] == 'Diplômante') &
                   (df['Dept'] == dept)]
        dept_data = dept_data.drop_duplicates(subset=['Matricule Etudiant'])
        total_dept_students = len(dept_data)
        # Nettoyer colonnes pour filtres
        dept_data['Date PV'] = pd.to_datetime(dept_data['Date PV'], errors='coerce')
        dept_data = dept_data.dropna(subset=['Date PV'])
        dept_data['Etudiant Actif'] = dept_data['Etudiant Actif'].str.strip().str.lower()
        # Filter out non-active students and those with registration after the closure date
        dept_dropout_data = dept_data[(dept_data['Type Formation'] == 'Diplômante')&
                                      (dept_data['Etudiant Actif'] == 'non') & 
                                      (dept_data['Date PV'] > pd.to_datetime(closure_date))]
        total_dept_non_active_students = len(dept_dropout_data)

        dept_reorientation_data = dept_data[(dept_data['Type Formation'] == 'Diplômante') &
                                            (dept_data['Etudiant Actif'] == 'non') & 
                                            (dept_data['Date PV'] > pd.to_datetime(closure_date)) & 
                                            (dept_data['Commentairesfs'].str.contains(r'(?i)\b(reo|réo|réorientation|reorientation)\b', regex=True, na=False))]
        total_dept_reorientation_students = len(dept_reorientation_data)

        total_dept_non_active_students = total_dept_non_active_students - total_dept_reorientation_students
        total_dept_active_students = total_dept_students - total_dept_non_active_students     

        dropout_dept_rate_1 = (total_dept_non_active_students / total_dept_students) * 100 if total_dept_students > 0 else 0
        dropout_dept_rate_2 = (total_dept_non_active_students / total_dept_active_students) * 100 if total_dept_active_students > 0 else 0
        dropout_dept_rate_percentage_1 = f"{dropout_dept_rate_1:.2f}%"
        dropout_dept_rate_percentage_2 = f"{dropout_dept_rate_2:.2f}%"

        # Store the result for the department
        department_results.append({
            "Dept": dept,
            "Total des stagiaires diplômantes": total_dept_students,
            "Stagiaires diplômantes actifs": total_dept_active_students,
            "Stagiaires diplômantes déperdus": total_dept_non_active_students,
            "Taux de déperdition des inactifs par total": dropout_dept_rate_percentage_1,
            "Taux de déperdition des inactifs par actifs": dropout_dept_rate_percentage_2
            })
    # Convert the results to a DataFrame
    department_df = pd.DataFrame(department_results)
    # Display the table to the user
    st.write("### Taux de déperdition par département")
    st.dataframe(department_df)
#############################################################################################################
    department_df['Taux de déperdition numérique'] = department_df['Taux de déperdition des inactifs par actifs'].str.rstrip('%').astype(float) # Conversion pour la visualisation : convertir en float
    fig_dept = px.pie(department_df,
                      names="Dept",
                      values="Taux de déperdition numérique",
                      title="📊 Taux de déperdition par Département",
                      labels={"Dept": "Département", "Taux de déperdition numérique": "Taux de déperdition (%)"}
                     )
    st.plotly_chart(fig_dept)
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
    # Display the table to the user
    st.write("### Taux de déperdition par établissement")
    st.dataframe(efp_df)  
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
    annees_etude = year_data['année Etude'].dropna().unique()
    annee_etude_results = []

    for annee_etude in annees_etude:
        annee_etude_data = df[(df['Année Scolaire'] == selected_year) &
                   (df['Type Formation'] == 'Diplômante') &
                   (df['année Etude'] == annee_etude)]
        annee_etude_data = annee_etude_data.drop_duplicates(subset=['Matricule Etudiant'])
        total_annee_etude_students = len(annee_etude_data)
        # Nettoyer colonnes pour filtres
        annee_etude_data['Date PV'] = pd.to_datetime(annee_etude_data['Date PV'], errors='coerce')
        annee_etude_data = annee_etude_data.dropna(subset=['Date PV'])
        annee_etude_data['Etudiant Actif'] = annee_etude_data['Etudiant Actif'].str.strip().str.lower()
        # Filter out non-active students and those with registration after the closure date
        annee_etude_dropout_data = annee_etude_data[(annee_etude_data['Type Formation'] == 'Diplômante')&
                                      (annee_etude_data['Etudiant Actif'] == 'non') & 
                                      (annee_etude_data['Date PV'] > pd.to_datetime(closure_date))]
        total_annee_etude_non_active_students = len(annee_etude_dropout_data)

        annee_etude_reorientation_data = annee_etude_data[(annee_etude_data['Type Formation'] == 'Diplômante') &
                                            (annee_etude_data['Etudiant Actif'] == 'non') & 
                                            (annee_etude_data['Date PV'] > pd.to_datetime(closure_date)) & 
                                            (annee_etude_data['Commentairesfs'].str.contains(r'(?i)\b(reo|réo|réorientation|reorientation)\b', regex=True, na=False))]
        total_annee_etude_reorientation_students = len(annee_etude_reorientation_data)

        total_annee_etude_non_active_students = total_annee_etude_non_active_students - total_annee_etude_reorientation_students
        total_annee_etude_active_students = total_annee_etude_students - total_annee_etude_non_active_students     

        dropout_annee_etude_rate_1 = (total_annee_etude_non_active_students / total_annee_etude_students) * 100 if total_annee_etude_students > 0 else 0
        dropout_annee_etude_rate_2 = (total_annee_etude_non_active_students / total_annee_etude_active_students) * 100 if total_annee_etude_active_students > 0 else 0
        dropout_annee_etude_rate_percentage_1 = f"{dropout_annee_etude_rate_1:.2f}%"
        dropout_annee_etude_rate_percentage_2 = f"{dropout_annee_etude_rate_2:.2f}%"

        # Store the result for the annee etude
        annee_etude_results.append({
            "année Etude": annee_etude,
            "Total des stagiaires diplômantes": total_annee_etude_students,
            "Stagiaires diplômantes actifs": total_annee_etude_active_students,
            "Stagiaires diplômantes déperdus": total_annee_etude_non_active_students,
            "Taux de déperdition des inactifs par total": dropout_annee_etude_rate_percentage_1,
            "Taux de déperdition des inactifs par actifs": dropout_annee_etude_rate_percentage_2
            })
    # Convert the results to a DataFrame
    annee_etude_df = pd.DataFrame(annee_etude_results)
    # Display the table to the user
    st.write("### Taux de déperdition par année étude")
    st.dataframe(annee_etude_df)
#############################################################################################################
    annee_etude_df['Taux de déperdition numérique'] = annee_etude_df['Taux de déperdition des inactifs par actifs'].str.rstrip('%').astype(float)
    fig_annee_etude = px.pie(annee_etude_df,
                      names="année Etude",
                      values="Taux de déperdition numérique",
                      title="📊 Taux de déperdition par année étude",
                      labels={"année Etude": "Année Etude", "Taux de déperdition numérique": "Taux de déperdition (%)"}
                     )
    st.plotly_chart(fig_annee_etude)
#############################################################################################################
    filieres = year_data['Code filière'].dropna().unique()
    filiere_results = []

    for filiere in filieres:
        filiere_data = df[(df['Année Scolaire'] == selected_year) &
                   (df['Type Formation'] == 'Diplômante') &
                   (df['Code filière'] == filiere)]
        filiere_data = filiere_data.drop_duplicates(subset=['Matricule Etudiant'])
        total_filiere_students = len(filiere_data)
        # Nettoyer colonnes pour filtres
        filiere_data['Date PV'] = pd.to_datetime(filiere_data['Date PV'], errors='coerce')
        filiere_data = filiere_data.dropna(subset=['Date PV'])
        filiere_data['Etudiant Actif'] = filiere_data['Etudiant Actif'].str.strip().str.lower()
        # Filter out non-active students and those with registration after the closure date
        filiere_dropout_data = filiere_data[(filiere_data['Type Formation'] == 'Diplômante')&
                                      (filiere_data['Etudiant Actif'] == 'non') & 
                                      (filiere_data['Date PV'] > pd.to_datetime(closure_date))]
        total_filiere_non_active_students = len(filiere_dropout_data)

        filiere_reorientation_data = filiere_data[(filiere_data['Type Formation'] == 'Diplômante') &
                                            (filiere_data['Etudiant Actif'] == 'non') & 
                                            (filiere_data['Date PV'] > pd.to_datetime(closure_date)) & 
                                            (filiere_data['Commentairesfs'].str.contains(r'(?i)\b(reo|réo|réorientation|reorientation)\b', regex=True, na=False))]
        total_filiere_reorientation_students = len(filiere_reorientation_data)

        total_filiere_non_active_students = total_filiere_non_active_students - total_filiere_reorientation_students
        total_filiere_active_students = total_filiere_students - total_filiere_non_active_students     

        dropout_filiere_rate_1 = (total_filiere_non_active_students / total_filiere_students) * 100 if total_filiere_students > 0 else 0
        dropout_filiere_rate_2 = (total_filiere_non_active_students / total_filiere_active_students) * 100 if total_filiere_active_students > 0 else 0
        dropout_filiere_rate_percentage_1 = f"{dropout_filiere_rate_1:.2f}%"
        dropout_filiere_rate_percentage_2 = f"{dropout_filiere_rate_2:.2f}%"

        # Store the result for the efp
        filiere_results.append({
            "Code filière": filiere,
            "Total des stagiaires diplômantes": total_filiere_students,
            "Stagiaires diplômantes actifs": total_filiere_active_students,
            "Stagiaires diplômantes déperdus": total_filiere_non_active_students,
            "Taux de déperdition des inactifs par total": dropout_filiere_rate_percentage_1,
            "Taux de déperdition des inactifs par actifs": dropout_filiere_rate_percentage_2
            })
    # Convert the results to a DataFrame
    filiere_df = pd.DataFrame(filiere_results)
    # Display the table to the user
    st.write("### Taux de déperdition par filière")
    st.dataframe(filiere_df)
#############################################################################################################
    filiere_df['Taux de déperdition (%)'] = filiere_df['Taux de déperdition des inactifs par actifs'].str.rstrip('%').astype(float) # Convertir la colonne en numérique
    fig_filiere = px.bar(filiere_df, 
                         x="Code filière", 
                         y="Taux de déperdition (%)", 
                         color="Code filière", 
                         barmode="group", 
                         width=4000,
                         height=600,
                         title="📊 Taux de déperdition par filière")
    fig_filiere.update_traces(width=0.8)
    fig_filiere.update_layout(xaxis_tickangle=-45,
                          margin=dict(l=40, r=40, t=80, b=150),
                          hovermode='x unified',
                          hoverdistance=100
                          )
    # Ordonner les barres pour avoir le plus grand taux en haut
    st.plotly_chart(fig_filiere) 

else:
    st.error("Aucune donnée disponible. Veuillez télécharger un fichier.")
