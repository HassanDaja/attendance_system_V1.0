import cv2
import streamlit as st
import av
import MOD
import streamlit_webrtc as webrtc

Model = MOD.Model
# Define the detect function to detect faces in a given frame
def detect(frame,Conf_rate=50):
    Model.conf = Conf_rate/100
    info = Model(frame)
    if info.xyxy[0] is not None:
        for face_info in info.pandas().xyxy[0].values.tolist():
            x = int(face_info[0])
            y = int(face_info[1])
            w = int(face_info[2] - face_info[0])
            h = int(face_info[3] - face_info[1])
            conf = face_info[4]
            # Crop the face from the image using the coordinates
            face_frame = frame[y:y+h, x:x+w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{conf:.2f}", (int(x), int(y) + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 3)
    return frame

# Define the ImageTransformer class to process video frames using the detect function
class ImageTransformer(webrtc.VideoProcessorBase):
    def __init__(self):
        super().__init__()

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        # Convert the video frame to a numpy array
        image = frame.to_ndarray(format="bgr24")

        # Call the detect function to detect faces in the video frame
        processed_image = detect(image)

        # Convert the processed video frame back to an av.VideoFrame object
        return av.VideoFrame.from_ndarray(processed_image, format="bgr24")

# Define the main function to create the UI and start the WebRTC video stream
def main():
    st.title("WebRTC Face Detection")

    # Create a WebRTC video stream using the streamlit-webrtc library
    RTC_CONFIGURATION = webrtc.RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )
    webrtc_ctx = webrtc.webrtc_streamer(
        key="opencv-filter",
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=ImageTransformer,
        async_processing=True,
        media_stream_constraints={'video':True,'audio':False}
    )

