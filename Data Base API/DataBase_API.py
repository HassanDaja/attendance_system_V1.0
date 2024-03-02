from flask import Flask, jsonify,request
import Database_methods as Database
app = Flask(__name__)
db=Database.db()
print(f"+++++++++++++{db.db_status}+++++++++++++++++")
@app.route('/Database/test', methods=['GET'])
def lol():
    return jsonify({'Value':1})
@app.route('/Database/get_students_info/<int:lecture_id>', methods=['GET'])
def get_info(lecture_id):
    names,encodings=db.get_all_students_info(lecture_id)
    return jsonify({'Names':names,"Encodings":encodings})

#    def student_signup(self,email, username, password, encodings):
@app.route('/Database/add_student_to_db',methods=['POST'])
def add_student_to_db():
    status=None
    message=None
    data=request.json
    email=data['email']
    username=data['username']
    password=data['password']
    encodings=data['encodings']
    results=db.student_signup(email,username,password,encodings)
    if results == 200:
        status = 'Success'
        message = 'Student has been added successfully.'
    elif results == 409:
        status = 'Error'
        message = 'Student already exists.'
    else:
        status = 'Error'
        message = 'An error occurred while adding the student to the database.'

    return jsonify({'status':status,'message':message})
@app.route('/Database/add_lec_to_db',methods=['POST'])
def add_lecture_to_db():
    data=request.json
    lec_id=data['lec_id']
    lec_name=data['lec_name']
    instructor_name=data['instructor_name']
    results=db.add_lecture(lec_id,lec_name,instructor_name)
    if results == 201:
        status = 'Success'
        message = 'Lecture has been added successfully.'
    elif results == 409:
        status = 'Error'
        message = 'lecture already exists.'
    else:
        status = 'Error'
        message = 'An error occurred while adding the lecture to the database.'
    return jsonify({'status': status, 'message': message})

@app.route('/Database/add_student_to_lec',methods=['POST'])
def add_student_to_lec():
    data=request.json
    lec_id=data['lec_id']
    student_id=data['student_id']
    results=db.add_student_to_lecture(student_id=student_id,lecture_id=lec_id)
    if results == 200:
        status = 'Success'
        message = f'Student has been added to lecture {lec_id} successfully.'
    elif results == 404:
        status = 'Error'
        message = "lecture doesn't exists."
    else:
        status = 'Error'
        message = f'An error occurred while adding the student to the Lecture {lec_id}.'
    return jsonify({'status': status, 'message': message})

if __name__ == '__main__':
    app.run(debug=True,port=5555    )