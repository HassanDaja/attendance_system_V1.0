import streamlit as st
from Methods import load_camera_frames
from CSS.Button import button_style
from Methods import Detect_from_db
import time
st.markdown(button_style,unsafe_allow_html=True,)
st.markdown("<h1 style='text-align: center'>Attendance Test Case</h1>", unsafe_allow_html=True)
left,mid,right=st.columns(3)
with mid:
    if st.button('Start test case'):
        with st.spinner('Getting the required data'):
            time.sleep(2)
            Frames = load_camera_frames()
            for frame in Frames:
                st.image(frame,channels='BGR')
                st.write("Attendance list")
                attendance,faces=Detect_from_db(frame,123)
                st.write(attendance)
                for face in faces:
                    st.image(face,channels='BGR')
