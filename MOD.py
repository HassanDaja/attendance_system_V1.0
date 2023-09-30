import torch
import streamlit as st
def load_model():
    model = torch.hub.load('yolov5','custom',path='Weights/face_detection_yolov5s.pt',source='local')
    return model
