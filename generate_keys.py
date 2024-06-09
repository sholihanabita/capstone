# import pickle
# from pathlib import Path

# import streamlit_authenticator as stauth
# names = ['Nab', 'Kelompok 8']
# usernames = ['nabb', 'kelompok8']
# passwords = ['nab123', '123']

# hashed_paswords = stauth.Hasher(passwords).generate()

# file_path = Path(__file__).parent / 'hashed_pw.pkl'
# with file_path.open('wb') as file:
#     pickel.dump(hashed_passwords, file)