import threading

from eye_detection import start_camera_session, main_eye_detection, finish_webcam_session
from buttonimages_app import ButtonimagesApp

def run_eyetracking():
    # Open the webcam first
    cap = start_camera_session()

    main_eye_detection(cap)

    # Make sure the webcam session is really finished
    finish_webcam_session(cap)

if __name__ == "__main__":

    # Create thread
    button_thread = threading.Thread(target=run_eyetracking)

    # Start the thread
    button_thread.start()

    app = ButtonimagesApp()
    app.run()

    #button_thread.join()