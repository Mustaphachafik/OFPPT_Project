import streamlit as st

# Page setup
home_page = st.Page(
    "homepage.py",
    title="Home Page",
    icon="🏠",
    default=True,
    )   
file_upload_page = st.Page(
    "views/file_upload.py",
    title="Upload",
    icon="📂",
    )
parametrage_page = st.Page(
    "views/efp_date_cloture.py",
    title="Parametrage",
    icon="⚙️",
    )
dashboard_page = st.Page(
    "views/dashboard.py",
    title="Dashboard",
    icon="📊",
    )

#navigation setup
pg = st.navigation(pages= [home_page, file_upload_page, parametrage_page, dashboard_page])
pg.run()
st.logo('images/OfpptLogo.png')