# import kivy module   
#import kivy 

from kivy.app import App
from kivy.uix.button import Button
#from kivy.uix.image import Image

# to change the kivy default settings we use this module config
#from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
#Config.set('graphics', 'resizable', True)

# Ensure a session can be closed by releasing the webcam
#from eye_detection import finish_webcam_session
#from eye_detection import get_camera_session
#cap = get_camera_session()
#finish_webcam_session(cap)

# This layout allows you to set relative coordinates for children.
from kivy.uix.relativelayout import RelativeLayout

# BoxLayout arranges children in a vertical or horizontal box.
# or help to put the children at the desired location.
#from kivy.uix.boxlayout import BoxLayout

""" # from eye_detection import current_time_milliseconds
from eye_detection import start_camera_session
from eye_detection import main_eye_detection
from eye_detection import finish_webcam_session """

# creating the root widget used in .kv file
""" class Buttonimages(BoxLayout):
    '''
        no need to do anything here as
        we are building things in .kv file
    '''
    pass """

class ButtonimagesApp(App):
    def build(self):

        # creating Relativelayout
        rl = RelativeLayout()
  
        # create an image a button
        # Adding images normal.png image as button
        # decided its position and size
        b1 = Button(text ="Push Me !",
                     color =(1, 0, .65, 1),
                     background_normal = '../images/placeholder1.png',
                     background_down ='../images/placeholder2.JPG',
                     size_hint = (.49, .49),
                     pos_hint = {'left':1, 'center_y':.5}
                   )

        b2 = Button(text ="Push Me Too !",
                     color =(1, 0, .65, 1),
                     background_normal = '../images/placeholder3.JPG',
                     background_down ='../images/placeholder2.JPG',
                     size_hint = (.49, .49),
                     pos_hint = {'right':1, 'center_y':.5}
                   )

        # adding button to widget
        rl.add_widget(b1)
        rl.add_widget(b2)
        #print(current_time_milliseconds())

        return rl

#def test_fkt():
#    print("this is a test")

if __name__ == '__main__':
    app = ButtonimagesApp()
    app.run()
    """ cap = start_camera_session()
    main_eye_detection(cap)

    # Make sure the webcam session is really finished
    finish_webcam_session(cap) """
    #print(current_time_milliseconds())
