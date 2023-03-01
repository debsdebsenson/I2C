"""
eye_detection module

Detection of the face and the exact location of the eyes.

# Eye detection:
Get frames in real time from the webcam to detect the eyes.

Find 68 specific landmarks of the face with the landmakrs approach
Left eye points: (36, 37, 38, 39, 40, 41)
Right eye points: (42, 43, 44, 45, 46, 47)

understanding dlib https://www.studytonight.com/post/dlib-68-points-face-landmark-detection-with-opencv-and-python
"""

# importing modules which will be required for simple eye detection
import cv2 # For image processing
import numpy as np
import dlib # Detection of facial landmarks
import os

# Function for calculation of the mid point of p1 and p2 that returns x and y
# coordinates of the midd point
def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

# TBD: make this more dynamically
# Path to the trained face recognition model
def model_path():

    # Create path
    pwd = os.path.dirname(__file__)
    trained_model = 'shape_predictor_68_face_landmarks.dat'
    return os.path.join(os.path.join(pwd, 'trained_models'), trained_model)

# Calculate the left, right, upper and lower points of the eye
def calcuate_eye_points(landmarks, landmark_points):

    left_point = (landmarks.part(landmark_points[0]).x, landmarks.part(landmark_points[0]).y)
    right_point = (landmarks.part(landmark_points[3]).x, landmarks.part(landmark_points[3]).y)
    center_top = midpoint(landmarks.part(landmark_points[1]), landmarks.part(landmark_points[2]))
    center_bottom = midpoint(landmarks.part(landmark_points[5]), landmarks.part(landmark_points[4]))
    return (left_point, right_point, center_top, center_bottom)

# Calculate the area of the eye from the frame with the landmarks and return it
# TBD: is this really needed? If so, replace landmark points with array values
# and call function 2x (for each eye)
def calculate_eye_area(landmarks, frame):
    calculated_eye_area = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                        (landmarks.part(37).x, landmarks.part(37).y),
                        (landmarks.part(38).x, landmarks.part(38).y),
                        (landmarks.part(39).x, landmarks.part(39).y),
                        (landmarks.part(40).x, landmarks.part(40).y),
                        (landmarks.part(41).x, landmarks.part(41).y)], np.int32)
    cv2.polylines(frame, [calculated_eye_area], True, 255, 2)
    return calculated_eye_area

# Mask creation of the eye
# TBD: understand what exactly this is used for
def mask_creation(frame, calculated_eye_area, gray):
    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [calculated_eye_area], True, 255, 2)
    cv2.fillPoly(mask, [calculated_eye_area], 255)
    eye_mask = cv2.bitwise_and(gray, gray, mask = mask)
    return eye_mask

# Cut out eye from face return calculated area of the whole eye
def extract_eye_area(calculated_eye_area, eye_mask):
    min_x = np.min(calculated_eye_area[:, 0])
    max_x = np.max(calculated_eye_area[:, 0])
    min_y = np.min(calculated_eye_area[:, 1])
    max_y = np.max(calculated_eye_area[:, 1])
    eye_area = eye_mask[min_y: max_y, min_x: max_x]
    return eye_area

# Extract the iris and pupil area from the whole eyes' area and return it
def extract_iris_and_pupil(eye_area):

    # Threshold for seperation of iris and pupil from the white part of the eye.
    #_, threshold_eye = cv2.threshold(eye_area, 70, 255, cv2.THRESH_BINARY)
    #cv2.resize(threshold_eye, None, fx = 5, fy = 5)

    # Calculate the area of the iris and pupil
    iris_and_pupil_area = cv2.resize(eye_area, None, fx = 5, fy = 5)
    return iris_and_pupil_area

# draw a cross on the screen on the eye
def draw_cross(frame, array_eye_points):

    # Creating the horizontal line
    cv2.line(frame, array_eye_points[0], array_eye_points[1], (0, 255, 0), 2)
    
    # Creating the vertical line
    cv2.line(frame, array_eye_points[2], array_eye_points[3], (0, 255, 0),2)

def left_right_side_division(threshold_eye):
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)
    return [left_side_white, right_side_white]

# The eye is divided into two parts to find out where more sclera is visible.
# If more of the sclera is visible on the right part, the person is gazing to
# the left. For this detection a conversion to a grayscale is done, a treshold
# is found and the white pixels are counted. The gaze ratio indicated where a
# specific eye is pointing at. 
# 
# TBD: This is not always the case and probably needs to be corrected later:
# "Normally both the eyes look in the same direction, so if we correctly detect
# the gaze of a single eye, we detect the gaze of both eyes. Only if we want to
# be more precise we could detect the gaze of both the eyes and use both values
# to detect the gaze ratio."
# There are several different cases to be covered here - also the case, that
# maybe only one eye is detected etc.

# Gaze direction detection
# TBD: the performance of this function is very poor and need to be improved
def get_gaze_ratio(eye_points_array, landmarks, frame, gray):

    #getting the area from the frame of the left eye only
    eye_region = np.array([(landmarks.part(eye_points_array[0]).x, landmarks.part(eye_points_array[0]).y),
                        (landmarks.part(eye_points_array[1]).x, landmarks.part(eye_points_array[1]).y),
                        (landmarks.part(eye_points_array[2]).x, landmarks.part(eye_points_array[2]).y),
                        (landmarks.part(eye_points_array[3]).x, landmarks.part(eye_points_array[3]).y),
                        (landmarks.part(eye_points_array[4]).x, landmarks.part(eye_points_array[4]).y),
                        (landmarks.part(eye_points_array[5]).x, landmarks.part(eye_points_array[5]).y)], np.int32)
    
    #cv2.polylines(frame, [eye_region], True, 255, 2)
    #height, width, _ = frame.shape

    #create the mask to extract xactly the inside of the left eye and exclude all the sorroundings.
    eye_mask = mask_creation(frame, eye_region, gray)
    
    #We now extract the eye from the face and we put it on his own window.Onlyt we need to keep in mind that wecan only cut
    #out rectangular shapes from the image, so we take all the extremes points of the eyes to get the rectangle
    calculated_eye_area = calculate_eye_area(landmarks, frame)
    eye_area = extract_eye_area(calculated_eye_area, eye_mask)
    
    #threshold to seperate iris and pupil from the white part of the eye.
    _, threshold_eye = cv2.threshold(eye_area, 70, 255, cv2.THRESH_BINARY)
    
    #dividing the eye into left_side and right_side.
    left_right_eye_side = left_right_side_division(threshold_eye)
    left_side_white = left_right_eye_side[0]
    right_side_white = left_right_eye_side[1]
    
    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio

# In this function the gaze direction is displayed
def display_gaze_direction(left_eye_points, right_eye_points, landmarks, frame, font, gray):
    gaze_ratio_left_eye = get_gaze_ratio(left_eye_points, landmarks, frame, gray)
    gaze_ratio_right_eye = get_gaze_ratio(right_eye_points, landmarks, frame, gray)
    
    average_gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
    
    if average_gaze_ratio <= 1:
        cv2.putText(frame, "RIGHT", (50, 100), font, 2, (0, 0, 255), 3)
        #new_frame[:] = (0, 0, 255) #blue
    elif 1 < average_gaze_ratio < 1.7:
        cv2.putText(frame, "CENTER", (50, 100), font, 2, (0, 0, 255), 3) #black
    else:
        #new_frame[:] = (255, 0, 0) #red
        cv2.putText(frame, "LEFT", (50, 100), font, 2, (0, 0, 255), 3)

# Loop to perform the eye detection
def eye_detection_loop(predictor, cap, detector):

    # Font of displayed text
    font = cv2.FONT_HERSHEY_PLAIN

    # Landmark points for the eyes
    left_eye_points = (36, 37, 38, 39, 40, 41)
    right_eye_points = (42, 43, 44, 45, 46, 47)
     
    while True:

        _,frame = cap.read()

        # Change the color of the frame captured by webcam to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # To detect faces from gray color frame
        faces = detector(gray)

        for face in faces:
            
            # Detection of the landmarks of a face
            landmarks = predictor(gray, face)
            
            #array_eye_points_left = calcuate_eye_points(landmarks, left_eye_points)
            #array_eye_points_right = calcuate_eye_points(landmarks, right_eye_points)

            #draw_cross(frame, array_eye_points_left)
            #draw_cross(frame, array_eye_points_right)

            #calculated_eye_area = calculate_eye_area(landmarks, frame)
            #eye_mask = mask_creation(frame, calculated_eye_area, gray)
            #eye_area = extract_eye_area(calculated_eye_area, eye_mask)
            #extract_iris_and_pupil(eye_area)

            display_gaze_direction(left_eye_points, right_eye_points, landmarks, frame, font, gray)

        # Display the image    
        cv2.imshow("Frame", frame)
        #cv2.imshow("EYE",eye)
        #cv2.imshow("THRESHOLD",threshold_eye)
        #cv2.imshow("LEFT_EYE",left_eye)
        #cv2.imshow("mask",mask)

        #close the webcam when escape key is pressed
        if cv2.waitKey(1) == 27:
            break

# Detect the face and then the area of the eye (therfore extract iris and 
def eye_detection(predictor, cap):

    # Use the detector to detect the frontal face
    detector = dlib.get_frontal_face_detector()

    # Detect the eye area
    eye_detection_loop(predictor, cap, detector)

# Function for releasing the webcam and closing all windows when session ends
def finish_webcam_session(cap):

    cap.release()
    cv2.destroyAllWindows()

def main_eye_detection():

    # For the detection of the facial landwark points
    predictor = dlib.shape_predictor(model_path())

    # Open webcab to capture the images, detect the eye and finish the session
    # afterwards.
    cap = cv2.VideoCapture(0)
    eye_detection(predictor, cap)
    finish_webcam_session(cap)

# call main function for the eye detection 
main_eye_detection()