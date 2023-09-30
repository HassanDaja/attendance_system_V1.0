from fastapi import FastAPI
from Database import get_all_students_encodings
app=FastAPI()

@app.get("/")
async def get_students_encodings():
    encodings=get_all_students_encodings(123)[0]["Face_encodings"]
    return encodings

