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

import os
import time  # For counting the time gazed at one side

# importing modules which will be required for simple eye detection
import cv2  # For image processing
import dlib  # Detection of facial landmarks
import numpy as np
import pyautogui  # For the mouse control - clicking on images
from pynput import keyboard

# from buttonimages_app import test_fkt

# test_fkt(cap)


# Function to get the current time in milliseconds
def current_time_milliseconds():
    return time.time() * 1000


# Fucntion for calculation a time difference
def calculate_time_difference(start_time, current_time):
    return round(current_time - start_time)


# Function for calculation of the mid point of p1 and p2 that returns x and y
# coordinates of the midd point
def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


# TBD: make this more dynamically
# Path to the trained face recognition model
def model_path():
    # Create path
    pwd = os.path.dirname(__file__)
    trained_model = "shape_predictor_68_face_landmarks.dat"
    return os.path.join(os.path.join(pwd, "trained_models"), trained_model)


# Calculate the left, right, upper and lower points of the eye
def calcuate_eye_points(landmarks, landmark_points):
    left_point = (
        landmarks.part(landmark_points[0]).x,
        landmarks.part(landmark_points[0]).y,
    )
    right_point = (
        landmarks.part(landmark_points[3]).x,
        landmarks.part(landmark_points[3]).y,
    )
    center_top = midpoint(
        landmarks.part(landmark_points[1]),
        landmarks.part(landmark_points[2]),
    )
    center_bottom = midpoint(
        landmarks.part(landmark_points[5]),
        landmarks.part(landmark_points[4]),
    )
    return (left_point, right_point, center_top, center_bottom)


# Calculate the area of the eye from the frame with the landmarks and return it
# TBD: is this really needed? If so, replace landmark points with array values
# and call function 2x (for each eye)
def calculate_eye_area(landmarks, frame):
    calculated_eye_area = np.array(
        [
            (landmarks.part(36).x, landmarks.part(36).y),
            (landmarks.part(37).x, landmarks.part(37).y),
            (landmarks.part(38).x, landmarks.part(38).y),
            (landmarks.part(39).x, landmarks.part(39).y),
            (landmarks.part(40).x, landmarks.part(40).y),
            (landmarks.part(41).x, landmarks.part(41).y),
        ],
        np.int32,
    )
    cv2.polylines(frame, [calculated_eye_area], True, 255, 2)
    return calculated_eye_area


# Mask creation of the eye
# TBD: understand what exactly this is used for
def mask_creation(frame, calculated_eye_area, gray):
    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [calculated_eye_area], True, 255, 2)
    cv2.fillPoly(mask, [calculated_eye_area], 255)
    eye_mask = cv2.bitwise_and(gray, gray, mask=mask)
    return eye_mask


# Cut out eye from face return calculated area of the whole eye
def extract_eye_area(calculated_eye_area, eye_mask):
    min_x = np.min(calculated_eye_area[:, 0])
    max_x = np.max(calculated_eye_area[:, 0])
    min_y = np.min(calculated_eye_area[:, 1])
    max_y = np.max(calculated_eye_area[:, 1])
    eye_area = eye_mask[min_y:max_y, min_x:max_x]
    return eye_area


# Extract the iris and pupil area from the whole eyes' area and return it
def extract_iris_and_pupil(eye_area):
    # Threshold for seperation of iris and pupil from the white part of the eye.
    # _, threshold_eye = cv2.threshold(eye_area, 70, 255, cv2.THRESH_BINARY)
    # cv2.resize(threshold_eye, None, fx = 5, fy = 5)

    # Calculate the area of the iris and pupil
    iris_and_pupil_area = cv2.resize(eye_area, None, fx=5, fy=5)
    return iris_and_pupil_area


# draw a cross on the screen on the eye
def draw_cross(frame, array_eye_points):
    # Creating the horizontal line
    cv2.line(frame, array_eye_points[0], array_eye_points[1], (0, 255, 0), 2)

    # Creating the vertical line
    cv2.line(frame, array_eye_points[2], array_eye_points[3], (0, 255, 0), 2)


def left_right_side_division(threshold_eye):
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0:height, 0 : int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0:height, int(width / 2) : width]
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
    # getting the area from the frame of the left eye only
    eye_region = np.array(
        [
            (
                landmarks.part(eye_points_array[0]).x,
                landmarks.part(eye_points_array[0]).y,
            ),
            (
                landmarks.part(eye_points_array[1]).x,
                landmarks.part(eye_points_array[1]).y,
            ),
            (
                landmarks.part(eye_points_array[2]).x,
                landmarks.part(eye_points_array[2]).y,
            ),
            (
                landmarks.part(eye_points_array[3]).x,
                landmarks.part(eye_points_array[3]).y,
            ),
            (
                landmarks.part(eye_points_array[4]).x,
                landmarks.part(eye_points_array[4]).y,
            ),
            (
                landmarks.part(eye_points_array[5]).x,
                landmarks.part(eye_points_array[5]).y,
            ),
        ],
        np.int32,
    )

    # cv2.polylines(frame, [eye_region], True, 255, 2)
    # height, width, _ = frame.shape

    # create the mask to extract xactly the inside of the left eye and exclude all the sorroundings.
    eye_mask = mask_creation(frame, eye_region, gray)

    # We now extract the eye from the face and we put it on his own window.Onlyt we need to keep in mind that wecan only cut
    # out rectangular shapes from the image, so we take all the extremes points of the eyes to get the rectangle
    calculated_eye_area = calculate_eye_area(landmarks, frame)
    eye_area = extract_eye_area(calculated_eye_area, eye_mask)

    # threshold to seperate iris and pupil from the white part of the eye.
    _, threshold_eye = cv2.threshold(eye_area, 70, 255, cv2.THRESH_BINARY)

    # dividing the eye into left_side and right_side.
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


def get_average_gaze_ratio(left_eye_points, right_eye_points, landmarks, frame, gray):
    gaze_ratio_left_eye = get_gaze_ratio(left_eye_points, landmarks, frame, gray)
    gaze_ratio_right_eye = get_gaze_ratio(right_eye_points, landmarks, frame, gray)

    average_gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
    # cv2.putText(frame, str(average_gaze_ratio), (200, 100), font, 2, (0, 255, 0), 3)
    return average_gaze_ratio


# get the time differnce while gazing/session is running
def get_time_difference_while_gazing_in_progress(
    previous_gaze_direction,
    gaze_direction,
    start_time,
):
    if previous_gaze_direction == gaze_direction:
        current_time = current_time_milliseconds()
        time_diff = calculate_time_difference(start_time, current_time)
    else:
        start_time = current_time_milliseconds()
        time_diff = 0
        print(f"_____Changed gaze direction at {start_time}______________")
    return time_diff, start_time


def click_on_selected_image(click_point):
    print(f"Calculated click point (x, y): {click_point}")


# Depnding on the gaze direction, the clickpoint on the screen is calculated
# here.
def calculate_click_point_on_screen(gaze_direction):
    # Get screen size and assign the values to the parameters
    screen_size = pyautogui.size()
    screen_size_x = screen_size[0]
    screen_size_y = screen_size[1]

    click_point_y = int(screen_size_y / 2)

    if gaze_direction == "LEFT":
        click_point_x = int(screen_size_x * (1 / 4))
    elif gaze_direction == "RIGHT":
        click_point_x = int(screen_size_x * (3 / 4))
    click_point = (click_point_x, click_point_y)
    print(
        f"Size of the selected screen: {screen_size} and gaze_direction {gaze_direction}",
    )
    return click_point


# TBD: This is only a placeholder function and has to be replaced later on
def event_when_5s_same_gaze_direction(time_diff, gaze_direction):
    if time_diff >= 5000:
        print(
            f"EVENT, gazed at one side for more tan 5s: {time_diff}, {gaze_direction}",
        )
        click_point = calculate_click_point_on_screen(gaze_direction)
        click_on_selected_image(click_point)

    """ def event_when_5ms_same_gaze_direction(time_diff, gaze_direction):
        #click_on_selected_image()
        calculate_click_point_on_screen(gaze_direction)
        # TBD: here the image that the person was looking  at for a certain
        # amount of time must be selected - also this function needs to be renamed """


# In this function the gaze direction is displayed
def display_gaze_direction(
    average_gaze_ratio,
    frame,
    font,
    previous_gaze_direction,
    start_time,
):
    if average_gaze_ratio <= 1:
        gaze_direction = "RIGHT"
        time_diff, start_time = get_time_difference_while_gazing_in_progress(
            previous_gaze_direction,
            gaze_direction,
            start_time,
        )
        cv2.putText(frame, gaze_direction, (50, 100), font, 2, (0, 0, 255), 3)
        # new_frame[:] = (0, 0, 255) #blue
    elif 1 < average_gaze_ratio < 1.7:
        gaze_direction = "CENTER"
        time_diff, start_time = get_time_difference_while_gazing_in_progress(
            previous_gaze_direction,
            gaze_direction,
            start_time,
        )
        cv2.putText(frame, gaze_direction, (50, 100), font, 2, (0, 0, 255), 3)  # black
    else:
        # new_frame[:] = (255, 0, 0) #red
        gaze_direction = "LEFT"
        time_diff, start_time = get_time_difference_while_gazing_in_progress(
            previous_gaze_direction,
            gaze_direction,
            start_time,
        )
        cv2.putText(frame, gaze_direction, (50, 100), font, 2, (0, 0, 255), 3)
    # print((time_diff, start_time))
    event_when_5s_same_gaze_direction(time_diff, gaze_direction)
    return gaze_direction, start_time


def key_detection(key):
    # close the webcam when escape key is pressed
    if key == keyboard.Key.esc:
        # finish_webcam_session(cap)
        # break
        return False


# Loop to perform the eye detection
def eye_detection_loop(predictor, cap, detector):
    # Font of displayed text
    font = cv2.FONT_HERSHEY_PLAIN

    # Landmark points for the eyes
    left_eye_points = (36, 37, 38, 39, 40, 41)
    right_eye_points = (42, 43, 44, 45, 46, 47)

    # Initialize previous_gaze_direction
    previous_gaze_direction = "CENTER"

    # Initialize start_time
    start_time = current_time_milliseconds()

    # Try to get the first frame, otherwise stop the session.
    if cap.isOpened():
        rval, frame = cap.read()
    else:
        rval = False
        raise IOError("Cannot open webcam")

    # callback = lambda key: key_detection(key, cap)

    # Collect events until released
    listener = keyboard.Listener(on_press=key_detection)
    listener.start()
    # Run this block while listener (keypress) is alive, otherwise terminate
    # this block.
    while True:
        _, frame = cap.read()

        # Change the color of the frame captured by webcam to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # To detect faces from gray color frame
        faces = detector(gray)
        # print("Test!")
        for face in faces:
            # Detection of the landmarks of a face
            landmarks = predictor(gray, face)

            # array_eye_points_left = calcuate_eye_points(landmarks, left_eye_points)
            # array_eye_points_right = calcuate_eye_points(landmarks, right_eye_points)

            # draw_cross(frame, array_eye_points_left)
            # draw_cross(frame, array_eye_points_right)

            # calculated_eye_area = calculate_eye_area(landmarks, frame)
            # eye_mask = mask_creation(frame, calculated_eye_area, gray)
            # eye_area = extract_eye_area(calculated_eye_area, eye_mask)
            # extract_iris_and_pupil(eye_area)

            # !!!!! TBD: function needs to be written where the time is
            # detected, how long someone is looking at left or right side. And
            # if person is 10s looking at one side, that side is selected.
            average_gaze_ratio = get_average_gaze_ratio(
                left_eye_points,
                right_eye_points,
                landmarks,
                frame,
                gray,
            )
            # get_time_gazed_at_one_side()
            gaze_direction, start_time = display_gaze_direction(
                average_gaze_ratio,
                frame,
                font,
                previous_gaze_direction,
                start_time,
            )
            previous_gaze_direction = gaze_direction

        # Display the image
        # cv2.imshow("Frame", frame)
        # cv2.imshow("EYE",eye)
        # cv2.imshow("THRESHOLD",threshold_eye)
        # cv2.imshow("LEFT_EYE",left_eye)
        # cv2.imshow("mask",mask)

        # close the webcam when escape key is pressed
        if not listener.is_alive():
            finish_webcam_session(cap)
            break

    # close keyboard listening thread
    listener.join()


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


def main_eye_detection(cap):
    # For the detection of the facial landwark points
    predictor = dlib.shape_predictor(model_path())

    # Open webcab to capture the images, detect the eye and finish the session
    # afterwards.
    eye_detection(predictor, cap)


def start_camera_session():
    cap = cv2.VideoCapture(0)
    return cap


# call main function for the eye detection
if __name__ == "__main__":
    # Open the webcam first
    cap = start_camera_session()

    main_eye_detection(cap)

    # Make sure the webcam session is really finished
    finish_webcam_session(cap)
    # app = ButtonimagesApp()
    # app.run()
