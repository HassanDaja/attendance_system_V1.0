from pymongo.mongo_client import MongoClient
import uuid
import urllib
from bson import ObjectId

class db:
    def __init__(self):
        self.db=None
        self.Load_DB()

    def Load_DB(self):
        username = urllib.parse.quote_plus('Hassandaja')
        password = urllib.parse.quote_plus('Hassankhaleddaja')
        try:
            print("Connecting Database ***********")
            uri = f"mongodb+srv://{username}:{password}@hassanscluster.chtpttu.mongodb.net/?retryWrites=true&w=majority"
            # Create a new client and connect to the server
            client = MongoClient(uri)
            # Send a ping to confirm a successful connection

            db = client['HassansCluster']
            self.db=db
            self.db_status=True
            return True
        except Exception as e:
            self.db_status = False
            return False
    def student_signup(self,email, username, password, encodings):
        db=self.db
        try:
            # Check if username or email already exist
            query = {'$or': [{'username': username}, {'email': email}]}
            existing_student = db['student_info'].find_one(query)
            if existing_student:
                return 409  # Conflict: Username or email already exists

            # Insert student data into the database
            student_id = str(uuid.uuid4())  # Generate a unique ID
            encodings=[array for array in encodings]
            Student_data = {
                '_id': student_id,
                'email': email,
                'username': username,
                'password': password,
                'Face_encodings': encodings
            }
            db['student_info'].insert_one(Student_data)
            return 200  # Success
        except Exception as e:
            print(e)
            return 500  # Internal server error

    def check_if_lecture_exist(self,lecture_id):
        db=self.db
        lecture=db.lecture_info.find_one({'_id':lecture_id})
        return lecture

    def add_lecture(self, lecture_id, lec_name, instructor):
        try:
            db = self.db

            # Check if lecture already exists
            if self.check_if_lecture_exist(lecture_id) is not None:
                return 409, 'Already exists'  # 409 Conflict: Resource already exists

            lecture_data = {
                '_id': lecture_id,
                'lecture_name': lec_name,
                'instructor': instructor,
            }

            db.lecture_info.insert_one(lecture_data)
            return 201  # 201 Created: Resource successfully created

        except Exception as e:
            print(e)
            return 500  # 500 Internal Server Error: Something went wrong on the server


    def add_student_to_lecture(self,student_id, lecture_id):
        try:
            db = self.db

            # Check if the lecture exists
            lecture_exists = db.lecture_info.find_one({'_id': lecture_id})
            if not lecture_exists:
                return 404  # Return an error code if the lecture doesn't exist

            student_encodings_cursor = db['student_info'].find({'_id': student_id}, {'Face_encodings': 1})
            student_encodings = list(student_encodings_cursor)
            student_encodings = student_encodings[0]['Face_encodings']
            db.lecture_info.update_one({'_id': lecture_id},
                                       {'$push': {'students_ids': student_id,
                                                  'students_encodings': {'$each': student_encodings}
                                                  }})
            return 200
        except Exception as e:
            print(e)
            return 500  # Return a different error code for general exceptions


    def get_faces_by_id(self,lecture_id):
        db = self.db
        students_encodings = db.lecture_info.find({'_id': lecture_id}, {'students_encodings': 1})
        return students_encodings

    def studentid_by_idx(self,lec_id,index):
        db =self.db
        students_ids = db.lecture_info.find({'_id': lec_id}, {'student_ids': 1})
        student_id=students_ids[index]
        return student_id

    def get_student_name(self, student_id):
        db = self.db

        # Retrieve the student information based on the student ID
        student_info = db.student_info.find_one({'_id': student_id}, {'username': 1})

        # Check if the student information was found
        if student_info:
            return student_info['username']
        else:
            # Handle the case where the student information is not found
            return None  # You might want to return a default value or raise an exception depending on your requirements
    def get_all_students_encodings(self,lec_id):
        db = self.db
        if not self.check_if_lecture_exist(lec_id):
            return 404
        students_encodings=db.lecture_info.find({'_id':lec_id},{'students_encodings':1})
        encodings=students_encodings[0]['students_encodings']
        return encodings
    def get_all_student_names(self,lec_id):
        names_list=[]
        all_ids=self.get_student_ids_by_lecture(lec_id)
        for id in all_ids:
            name=self.get_student_name(id)
            if name is not None:
                names_list.append(name)
        return names_list
    def get_all_students_info(self,lecture_id):
        print("Request_sent*************")
        names=self.get_all_student_names(lecture_id)
        encodings=self.get_all_students_encodings(lecture_id)
        return names,encodings
    def get_student_ids_by_lecture(self,lec_id):
        db=self.db
        results=db.lecture_info.find({'_id':lec_id},{'students_ids':1})
        list_results=list(results)
        # Extract the 'students_ids' field from the first document (assuming there is only one)
        students_ids = list_results[0].get('students_ids', [])
        return students_ids
    def get_username_by_id(self,student_id):
        db=self.db
        result = self.db.student_info.find_one({"_id": student_id },{'username':1})
        if result:
            return result.get('username')
        else:
            return False


