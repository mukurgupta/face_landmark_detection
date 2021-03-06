#Improritng necessary libraries
import cv2
import json
import dlib
import numpy as np
import pandas as pd

#Function to detect all the faces in an image and return the list of all the faces. 
#It takes uses grayscale image and an inbuilt function in dlib library
def detect_faces(gray_image):
    face_detect = dlib.get_frontal_face_detector()
    faces_list = face_detect(gray_image,0)
    
    return faces_list

#This Function predicts the coordinates of all the 68 coordinates in each face and returns a dictionary, where each Key corresponds to a face and value corresponds to the 68 identified landmarks
#It uses grayscale image as well, and takes the list of faces generated by earlier function as an input
#This function also creates the curve around the jaw line of the face by highlighting the landmarks from 1 to 17 on each face
def landmarks_coordinates(faces_list,gray_image):
    final_dict={}
    count=1
    
    landmarks_predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    
    
    for x in faces_list:
        landmarks=landmarks_predict(gray_image, x)
        #print(landmarks)

        landmarks_list = []

        for i in range(0, landmarks.num_parts):
            landmarks_list.append((landmarks.part(i).x, landmarks.part(i).y))
 
        for coord in landmarks_list[0:17]:
            cv2.circle(img, (coord[0], coord[1]), 8, (255, 255, 255), -1)

        final_dict['face_'+str(count)]=landmarks_list
        count=count+1
    
    return final_dict

#Function to show up the final image after creating a curve around the jawline
#Image is opened in a new window and will close if any key is pressed
def add_implement(img):
    cv2.namedWindow('img_jaw_line',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img_jaw_line', 600,600)

    cv2.imshow('img_jaw_line',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#This is the main driver code which will take the image as an input by taking it's path from the user.
#Then calling all the functions wherever needed
#And, lastly converting the final landmark coordinates in face(s) in an image into a Json and excel file.

path = input("Enter the path of the image: ")
img= cv2.imread(path)
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces_list = detect_faces(gray_image)

final_dict = landmarks_coordinates(faces_list,gray_image)


with open('final_feature_values.json', 'w') as temp_file:
    json.dump(final_dict, temp_file, indent=4)


pd.DataFrame(final_dict).to_excel("final_dict.xlsx")

print ('\nJson and excel file created in the folder. \nNow creating the image with the jaw line.Press any key to exit.')

add_implement(img)

print ('\nProcess complete.')




