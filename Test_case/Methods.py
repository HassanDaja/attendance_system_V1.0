from face_detector import YoloDetector
import numpy as np
import face_recognition
import cv2
from Database import get_all_students_info

def get_all_faces_encoded(img):
    model=YoloDetector(target_size=1080,device='cuda:0',min_face=10)
    encoded_faces=[]
    cropped_faces=[]
    pred_img=np.array(img)
    bboxes,points=model.predict(pred_img)
    for box in bboxes[0]:
        x1,y1,x2,y2=box
        cropped_face=img[y1:y2,x1:x2]
        cropped_faces.append(cropped_face)
        encdoed_face=face_recognition.face_encodings(cropped_face)
        if len(encdoed_face)>0:
            encoded_faces.append(encdoed_face[0])
    return encoded_faces,cropped_faces
def get_person_name(names,encodings,target):
    match=face_recognition.compare_faces(encodings,target,tolerance=0.6)
    indecies=np.where(match)
    if len(indecies[0])>0:
        index=match.index(True)
        name_index=index//3
        return names[name_index]
    return 'Unknown'

def Detect(img,lec_id=0):
    attended_students=[]
    encoded_faces,cropped_faces=get_all_faces_encoded(img)
    names=['hassan','abood','basel','khaled']
    encodings=np.load('Test_case/encodings.npy')
    for face in encoded_faces:
        name=get_person_name(names,encodings,face)
        if name!='Unknown':
            attended_students.append(name)
    return attended_students,cropped_faces

def Detect_from_db(img,lecture_id):
    attended_students=[]
    encoded_faces,cropped_faces=get_all_faces_encoded(img)
    names,students_encodings=get_all_students_info(lecture_id)
    for face in encoded_faces:
        name=get_person_name(names,students_encodings,face)
        if name!='Unknown':
            attended_students.append(name)
    return attended_students,cropped_faces
def load_camera_frames():
    imgs=[]
    imgs_path = 'Camera_frames/img'
    for i in range(1,4):
        img=cv2.imread(f'{imgs_path}{i}.png')
        imgs.append(img)
    return imgs
'''
import streamlit as st
img_path='Test_case/Camera_frames/img2.png'
img=cv2.imread(img_path)
attendance,cropped_faces=Detect_from_db(img,123)
st.write(attendance)
for face in cropped_faces:
    st.image(face,channels='BGR')
    '''
