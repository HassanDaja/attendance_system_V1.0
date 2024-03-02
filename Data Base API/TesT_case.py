import requests
def get_all_students_info(lecture_id):
    url = "http://127.0.0.1:5555"
    endpoint=f"/Database/get_students_info/{lecture_id}"
    req=requests.get(url+endpoint)
    names=req.json()['Names']
    encodings=req.json()['Encodings']
    return names,encodings
print(len(get_all_students_info(123)[1]))
