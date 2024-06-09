import pickle
from pathlib import Path
import streamlit_authenticator as stauth

import joblib
import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
from time import sleep
import pandas as pd
import sqlite3
import openai

# Muat pipeline yang telah disimpan
pipeline = joblib.load('MLMentalHealth.sav', 'rb')

# sidebar for navigation
with st.sidebar:
    selected = option_menu('Mental Health Prediction System',
                        [
                            'Home Page',
                            'Mental Health Prediction',
                            'Chat Bot'
                        ],
                        icons=['activity', 'heart','chat' ,'person'],
                        default_index=0)
    logout = st.button("Log out")

# Handle logout
if logout:
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("login.py")

# Input fields
if selected == 'Mental Health Prediction':
    #Gender Input
    # Kode Streamlit Anda
    st.title('Prediksi Diagnosis Kesehatan Mental')
    Gender = st.selectbox("Choose your gender",
        ("Male", "Female"),
        index=None)
    if Gender == "Male":
        Gender = 1
    else:
        Gender = 0
    
    # Age Input
    Age = st.number_input('Usia', min_value=0)

    # Year Input
    Year = st.selectbox("Your current year of Study?",
        ("Year 1", "Year 2", "Year 3", " Year 4"),
        index=None)
    if Year =="Year 1":
        Year = 0
    elif Year == "Year 2":
        Year = 1
    elif Year == "Year 3":
        Year = 2
    else:
        Year = 3   

    # CGPA Input
    CGPA = st.number_input('IPK', min_value=0.0, max_value=4.0, format="%.2f")

    # Marital Input
    Marital_Status = st.selectbox('Marital status',
        ("Yes", "No"),
        index=None)
    if Marital_Status == "Yes":
        Marital_Status = 1
    else:
        Marital_Status = 0

    # Depression Input
    Depression = st.selectbox('Do you have Depression?',
        ("Yes", "No"),
        index=None)
    if Depression == "Yes":
        Depression = 1
    else:
        Depression = 0

    # Anxiety Input
    Anxiety = st.selectbox('Do you have Anxiety?',
        ("Yes", "No"),
        index=None)
    if Anxiety == "Yes":
        Anxiety = 1
    else:
        Anxiety = 0

    # Pannic Attac Input
    Panic_Attack = st.selectbox('Do you have Panic attack?',
        ("Yes", "No"),
        index=None)
    if Panic_Attack == "Yes":
        Panic_Attack = 1
    else:
        Panic_Attack = 0
            
    # Prediksi saat tombol ditekan
    if st.button('Prediksi'):
        # Gabungkan input ke dalam satu dataframe
        input_data = pd.DataFrame([[Gender, Age, Year, CGPA, Marital_Status, Depression, Anxiety, Panic_Attack]],
                                columns=['Gender', 'Age', 'Year', 'CGPA', 'Marital_Status', 'Depression', 'Anxiety', 'Panic_Attack'])
        
        # Lakukan prediksi
        mental_predic = pipeline.predict(input_data)
        if mental_predic == 0:
            st.text("You are not suffering from any mental health issue.")
        else:
            st.text("You are suffering from some mental health issue. \nPlease take care of yourself by consulting a doctor.")

#Home Page
elif selected == 'Home Page':
    st.title("Welcome to Menti Check")
    st.write("""
    The aim of this project is to help individuals understand the seriousness of their mental health condition and provide guidance on whether they need professional help or not. This application can be used by students and college students.""")
    st.image("https://workplacedna.net/application/files/9016/1218/7136/Bipolar.jpg", caption='World Mental Health Day')
    st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Times New Roman'; color: #11111; font-weight: bold; text-align: center} 
            .center-text{
                text-align: center; 
}
            }
            </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Our Mission</p>', unsafe_allow_html=True)
    st.markdown('<p class="center-text">Recognized as a transparent and trustworthy nonprofit provider of quality health information.</p>', unsafe_allow_html=True)
    
    
    
    
    row1 = st.columns(2)
    row2 = st.columns(2)
    missions = [
        {
            "title": "Guidance you can trust",
            "image": "https://www.helpguide.org/wp-content/uploads/Frame-13794.png",
            "text": "Find trustworthy information about mental health and wellness that you can use to make better decisions."
        },
        {
            "title": "Skills for life success",
            "image": "https://www.helpguide.org/wp-content/uploads/Frame-13795-1.png",
            "text": "Build skills to manage your emotions, strengthen your relationships, and cope with difficult situations."
        },
        {
            "title": "Strategies to feel better",
            "image": "https://www.helpguide.org/wp-content/uploads/Frame-13791.png",
            "text": "Learn how to improve your mental health and well-being—and help your friends and family do the same."
        },
        {
            "title": "Support you can rely on",
            "image": "https://www.helpguide.org/wp-content/uploads/Frame-13793.png",
            "text": "As a free online resource, we’re here for you, day or night, whenever you need guidance, encouragement, or support."
        }
    ]
    
    for i, col in enumerate(row1 + row2):
        
        if i < len(missions):
            with col:
                st.image(missions[i]["image"], width=120)
                st.subheader(missions[i]["title"])
                st.write(missions[i]["text"])
        else:
            col.empty()
 
# Chatbot
elif selected == 'Chat Bot':
    st.title('What I Can Help You Today?')
    # with st.chat_message(name = 'assistant', avatar = '👩🏻‍⚕️'):
    #     st.write("Hello👋🏻")
    openai.api_key = st.secrets['OPENAI_API_KEY']
    
    if "openai_model" not in st.session_state:
        st.session_state['openai_model'] = 'gpt-3.5-turbo'
        
    #chat History
    if "messages" not in st.session_state:
        st.session_state.message = []
    
    #display Chat message
    for message in st.session_state.message:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    
    prompt = st.chat_input('What I Can Help You Today?')
    #reach user input
    if prompt:
        #display user
        with st.chat_message('user'):
            st.markdown(prompt)
        st.session_state.message.append({'role':'user', 'content':prompt})
        
        response = f'Echo: {prompt}'
        #display
        # Create a chat message placeholder for displaying the assistant's response
        with st.chat_message('assistant', avatar='👩🏻‍⚕️'):
            message_placeholder = st.empty()

            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state['openai_model'],
                messages=[
                    {'role': m['role'], 'content': m['content']}
                    for m in st.session_state.message
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get('content', '')
                message_placeholder.markdown(full_response + '|')
            message_placeholder.markdown(full_response)
    
        st.session_state.message.append({'role':'assistant', 'content':full_response})         


