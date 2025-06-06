import streamlit as st
st.set_page_config(page_title="Statistics Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Résumé")
st.write("""
    Cette application permet de calculer le taux de déperdition des étudiants de l'OFPPT. 
    Elle analyse les données d'inscription et de statut des étudiants pour calculer le taux de déperdition 
    basé sur la non-activité après la date de clôture de l'année scolaire.
""")
