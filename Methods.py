import streamlit

import Database
from PIL import Image
import face_recognition as FR
from MOD import load_model
import numpy as np

Model = None

def encode_face(img):
  face_encoding = FR.face_encodings(img)
  if len(face_encoding) > 0:
    return face_encoding[0]
  else:
    return False

def img_crop(img, bbox):
  x1, y1, x2, y2 = map(int, bbox)
  cropped_img = img.crop((x1, y1, x2, y2))
  return np.array(cropped_img)

def find_bbox(img):
  Model=load_model()
  result = Model(img)
  object_data = list(result.pandas().xyxy[0].values)
  if len(object_data) ==1 :
    bbox = list(map(int, object_data[0][:4]))
    return bbox
  return False

def get_encoding(img):
    bbox = find_bbox(img)
    if not bbox:
        return False
    cropped_img = img_crop(img, bbox)
    face_enc=encode_face(cropped_img)
    return face_enc

def images_for_same_perosn(image_encodings):

    # Compare the face encodings pairwise
    distance_threshold = 0.6  # Adjust as per your application
    matches = []
    for i in range(2):
        for j in range(i+1, 3):
            distance = FR.face_distance([image_encodings[i]], image_encodings[j])[0]
            matches.append(distance <= distance_threshold)

    # Determine if all pairwise comparisons match
    all_match = all(matches)
    return all_match

def check_person_imgs(imgs):
    imgs=map(Image.open,imgs)
    encodings=[]
    for img in imgs:
        encoding=get_encoding(img)
        if encoding is False:
            return False
        encodings.append(encoding)
    if not images_for_same_perosn(encodings):
        return False
    return encodings

def get_Student_index(encodings_list,face_encoding):
    match=FR.compare_faces(encodings_list,face_encoding)
    match_index = np.argmax(match) if np.any(match) else -1  # Default value -1 if no match found
    return match_index//3

def remove_duplicate(imgs):
    hash_set=set()
    imgs_list=[]
    for img in imgs:
        opened_img=Image.open(img)
        img_hash=hash(opened_img.tobytes())
        if img_hash not in hash_set:
            hash_set.add(img_hash)
            imgs_list.append(img)
    return imgs_list

def Add_student(email,username,pwd,encodings):
    status_msg=Database.student_signup(email,username,pwd,encodings)
    return status_msg







