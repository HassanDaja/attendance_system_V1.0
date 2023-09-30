import streamlit as st
import re
from Methods import check_person_imgs,Add_student
def display_imgs(imgs):
    if len(imgs)<=3:
        # Create a container to hold the images
        container = st.container()

        # Display the images inside the container
        with container:
            st.subheader("Uploaded Images")
            for idx, image in enumerate(imgs):
                st.image(image, caption=f"Uploaded Image {idx + 1}", width=150)
    else:
        st.error('Upload three images')
def return_first_three(imgs):
    return imgs[:3]
def image_Check_display(uploaded_files):
    if len(uploaded_files) == 3:
        return True
    st.error('Please upload three images of your face.')
    return False
def passowrd_comparing(password1,passowrd2):
    return password1==passowrd2

def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Use the re.match() function to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        st.error('incorrect Email,please try to enter another Email')
        return False
def is_valid_username(username):
    # Check if the username is at least 6 characters long.
    if len(username) < 6:
        st.error('The length of the username should be more than 6 letters')
        return False

    # Check if the username only contains letters, numbers, and underscores.
    if not re.match("^[a-zA-Z0-9_]+$", username):
        st.error('The user should only contain letters,numbers and _')
        return False

    # Check if the username does not contain any spaces or hyphens.
    if " " in username or "-" in username:
        st.error('The username contains space(" ") or "-"')
        return False

    return True

def is_valid_password(password):
    # Check if the password is at least 8 characters long.
    if len(password) < 8:
        st.error('the password should be longer that 8 letters.')
        return False

    # Check if the password contains at least one uppercase letter, one lowercase letter, and one digit.
    if not re.search(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)", password):
        st.error('The password should contain at least one: Uppercase letter,Lowercase letter and a digit.')
        return False

    # Check if the password does not contain any spaces or special characters.
    if re.search(r"\s|\W", password):
        st.error('password contains spaces or special characters which is not allowed.')
        return False

    return True


def sign_up_process(email,username,password1,password2,imgs):
    if not validate_email(email):
        return

    if not is_valid_username(username):
        return
    if not is_valid_password(password1):
        return
    if not passowrd_comparing(password1,password2):
        st.error("Passwords do not match. Please enter the same password again.")
        return
    if not image_Check_display(imgs):
        return
    encodings=check_person_imgs(imgs)
    if not encodings:
        st.error("The images Doesn't belong to the same person.")
        return
    sign_up_info=Add_student(email, username, password1, encodings)##will return status code and the message
    if sign_up_info[0]=='Success':
        st.success(sign_up_info[1])
        return
    else:
        st.error(f'{sign_up_info[0]},{sign_up_info[1]}')
