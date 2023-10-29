import Database
from PIL import Image
import numpy as np


def Get_Status_and_encodings(imgs):
    URL='http://192.168.1.128:8833'
    ENDPOINT='/check_person_images'
    import requests
    imges=[]
    for img in imgs:
        image=Image.open(img)
        image=image.resize((image.width//3,image.height//3))
        image_array=np.array(image)
        imges.append(image_array.tolist())
    print("Request sent")
    results=requests.post(URL+ENDPOINT,json={'imgs':imges})
    data=results.json()
    return  data['Status'],data['Data']

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







