import requests
url="http://127.0.0.1:5555"


def student_signup(email, username, password, encodings):
    encodings = [array.tolist() for array in encodings]
    data = {'email': email, 'username': username, 'password': password, 'encodings': encodings}
    req = requests.post(f"{url}/Database/add_student_to_db",json=data)
    status = req.json()['status']
    message = req.json()['message']
    return status, message
def get_all_students_info(lecture_id):
    endpoint=f"/Database/get_students_info/{lecture_id}"
    req=requests.get(url+endpoint)
    names=req.json()['Names']
    encodings=req.json()['Encodings']
    return names,encodings

