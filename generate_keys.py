import pickle
import bcrypt
from pathlib import Path
import streamlit_authenticator as stauth

names = ["Jihane Habati", "Soufiane Souhail"]
usernames = ["jjihane", "ssouhail"]
passwords = ["Bluemoon@55", "Redmoon@55"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

 #run with """"python generate_keys.py