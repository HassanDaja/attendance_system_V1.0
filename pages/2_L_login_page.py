import streamlit as st
from CSS.Button import button_style
st.markdown("<h1 style='text-align: center'>Log in</h1>", unsafe_allow_html=True)
left,right= st.columns(2)

with left:
    mail=st.text_input('Email')
with right:
    pwd=st.text_input('Password',type='password')
no1,mid,no2=st.columns(3)
with mid:
    submit=st.button('Submit')
    st.write("New Account [Sign up](http://localhost:8501/Sign_up)")

st.markdown(button_style, unsafe_allow_html=True)