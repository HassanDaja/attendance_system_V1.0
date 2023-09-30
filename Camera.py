import streamlit as st
import cv2
import time
from Cam_test import detect
Detect=st.button('Detect')
Start=st.button('Start')
Stop=st.button('Stop')
Conf_Rate= st.slider("Conf_Rate", min_value=1, max_value=100, step=1,value=1)
if Start:
    cam=cv2.VideoCapture(0)
    Frame_window=st.image([])
    face_frame=[]
    while True:
        status,frame=cam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if Detect:
            frame=detect(frame,Conf_Rate)
        if Stop:
            Start=False
            break
        Frame_window.image(frame)
        time.sleep(.05)
else:
    st.write('Waiting For Capture')




