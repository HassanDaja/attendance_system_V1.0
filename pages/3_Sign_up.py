import time
import streamlit as st
from CSS.Button import button_style
from sign_up_func import sign_up_process, display_imgs, return_first_three
from Methods import remove_duplicate
st.markdown(button_style, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center'>Sign up</h1>", unsafe_allow_html=True)
mail = st.text_input('Email')
username = st.text_input('Username')
pwd = st.text_input('Password', type='password')
re_pwd = st.text_input('Re-type Password', type='password')

left, right = st.columns(2)
with left:
    uploaded_files = st.file_uploader("Choose three image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="file_uploader")
with right:
    if uploaded_files:
        uploaded_files=return_first_three(uploaded_files)
        uploaded_files=remove_duplicate(uploaded_files)
        display_imgs(uploaded_files)
st.write("You already have an account? [Log in](http://localhost:8501/L_login_page)")

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("Sign up"):
        with st.spinner("Signing up..."):
            sign_up_process(email=mail, username=username, password1=pwd, password2=re_pwd, imgs=uploaded_files)

