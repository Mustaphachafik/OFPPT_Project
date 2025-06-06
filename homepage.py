import streamlit as st
import hashlib

# Simulate a base of users with hashed passwords
users = {
    "jihane habati": hashlib.sha256("Bluemoon@55".encode()).hexdigest()
}
# Hashing function to compare the input password with the stored one
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
# Function to check login credentials
def check_login(username, password):
    if username in users and users[username] == hash_password(password):
        return True
    return False

# Page configuration
col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.image('images/OfpptLogo.png', width=170)
with col2:
    st.title("Taux de Déperdition des Stagiaires")

# Check if the user is authenticated
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
# If not authenticated, show the login form
if not st.session_state.authenticated:
    st.write("\n")
    st.title("🔐 Connexion requise")
    with st.form("login"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")
        if submitted:
            if check_login(username, password):
                st.session_state.authenticated = True  # Set user as authenticated
                st.session_state.username = username  # Store username in session state
                st.success("Connexion réussie!")
                st.rerun()  # Refresh to show the main app after login
            else:
                st.error("Identifiants incorrects.")
else:
    # If authenticated
    st.sidebar.button("🔒 Se déconnecter", on_click=lambda: st.session_state.update({"authenticated": False}))
    st.write("Utilisez le menu à gauche pour naviguer")
    
