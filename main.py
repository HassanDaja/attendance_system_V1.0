import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='Home Page',page_icon='imgs/Main/Logo.png',layout="wide")
st.title('Welcome')
ContactUs = st.button('Contact us')
if st.button('Log in'):
    switch_page("l login page")
if ContactUs:
    switch_page('C Contact')