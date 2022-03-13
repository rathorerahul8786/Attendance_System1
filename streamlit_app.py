import csv
import streamlit as st
from PIL import Image# to read & resize the image 

import time
import cv2
import pickle
from Preparing import prepare_test_img, test

t0= time.time()
print("Hello")

# Declaring variables
path = "db"




def main():
    # Loading the mode
    @st.cache
    def load_model():
        with open ('encoded_faces.pickle', 'rb') as f_in:
            encoded_trains = pickle.load(f_in)
        return encoded_trains
    encoded_trains = load_model()

    # Start of the project
    st.title("Attendance_Project")
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",
    ["Attend from image", "Attend using camera", "Training"])

    if app_mode == "Attend from image":     
        attendance_file = st.file_uploader("Choose attendance file",type =['csv'])
        uploaded_file = st.file_uploader("Upload a picture of a person to make him attend", type=['jpg', 'jpeg', 'png'])
        if attendance_file is not None and uploaded_file is not None:   

            st.title("Here is the picture you've uploded")
            test_img, encoded_tests, face_test_locations = prepare_test_img(uploaded_file)
            now = time.localtime()
            date = time.strftime("%Y/%m/%d", now)
            new_date = st.text_input('For Trying purposes you can put any date to test the program', date)
            attendance_list, df = test(encoded_tests, face_test_locations, test_img, encoded_trains, attendance_file, new_date)
            t1 = time.time() - t0
            st.write("Time elapsed: ", t1)
            # test_img = cv2.resize(test_img,(0,0),None,0.50,0.50) 
            # cv2.imshow('Test',test_img)
            # cv2.waitKey(0)
            st.image(test_img)
            #st.write(attendance_list)
            st.write(df)





    elif app_mode == "Attend using camera":
        attendance_file = st.file_uploader("Choose attendance file",type =['csv'])
        picture = st.camera_input("Take a picture")
        if picture is not None and attendance_file is not None:
            st.title("Here is the picture you've taken")
            #img = Image.open(picture)

            test_img, encoded_tests, face_test_locations = prepare_test_img(picture)

            attendance_list, df = test(encoded_tests, face_test_locations, test_img, encoded_trains, attendance_file)

            t1 = time.time() - t0
            st.write("Time elapsed: ", t1)
            #test_img = cv2.resize(test_img,(0,0),None,0.50,0.50) 
            st.image(test_img)
            #cv2.imshow('Test',test_img)
            #cv2.waitKey(0)
        
            #st.write(attendance_list)
            st.write(df)



    elif app_mode == "Training":
        st.subheader('Training Steps:')
        st.markdown("1. Get a photo of every employee with **only one face** in the picture.")
        st.markdown('2. Put all the photos in the **db** folder')
        st.markdown("3. Press **Train The Model** Button")
        if st.button("Train The Model"):
            from Training import training
            encoded_trains = training(path)


#error handler
#st.set_option('deprecation.showPyplotGlobalUse', False)

if __name__=='__main__':
    main()