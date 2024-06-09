import streamlit as st
from time import sleep


# Tampilan utama aplikasi
st.title("Welcome to Menti Check")
st.write("Please log in to continue (username `admin`, password `admin`).")            

# Halaman Login
st.title("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Log in", type="primary"):
    if username == "admin" and password == "admin":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.experimental_rerun()
    else:
        st.error("Incorrect username or password")

# Mengalihkan ke halaman lain jika berhasil login
if 'logged_in' in st.session_state and st.session_state.logged_in:
    st.switch_page("pages/app.py")  # Nama halaman yang sesuai