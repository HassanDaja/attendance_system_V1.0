class student():
    def __init__(self,email,username,passwords,encodings):
        self.email=None
        self.username=None
        self.password=None
        self.encodings=None
    def set_student_info(self,email,username,passwords,encodings):
        self.email=email
        self.username=username
        self.password=passwords
        self.encodings=encodings
    def get_email(self):
        return self.email
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    def get_encodings(self):
        return self.encodings
    def return_student_data(self):
        email=self.get_email()
        username=self.get_username()
        password=self.get_password()
        encodigns=self.get_encodings()
        return [email,username,password,encodigns]
