# import kivy module   
#import kivy 

from kivy.app import App
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
#from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# BoxLayout arranges children in a vertical or horizontal box.
# or help to put the children at the desired location.
#from kivy.uix.boxlayout import BoxLayout

from eye_detection import current_time_milliseconds
from eye_detection import calculate_time_difference

import time

"""
from eye_detection import start_camera_session
from eye_detection import main_eye_detection
from eye_detection import finish_webcam_session """

class SessionLayout(GridLayout):

    # Constructor which takes x keyword arguments as input.
    def __init__(self, **kwargs):
        super(SessionLayout, self).__init__(**kwargs)
        self.cols = 2        

        self.b1 = Button(text ="Push Me !",
                     color =(1, 0, .65, 1),
                     background_normal = '../images/placeholder1.png',
                     background_down ='../images/placeholder2.JPG',
                     size_hint = (.49, .49),
                     pos_hint = {'left':1, 'center_y':.5}
                   )

        # Add an event when this button is pressed
        self.b1.bind(on_press=self.pressed_time)
        self.add_widget(self.b1)

        self.b2 = Button(text ="Push Me Too !",
                     color =(1, 0, .65, 1),
                     background_normal = '../images/placeholder3.JPG',
                     background_down ='../images/placeholder2.JPG',
                     size_hint = (.49, .49),
                     pos_hint = {'right':1, 'center_y':.5}
                   )
        
        # Add an event when this button is pressed
        self.b2.bind(on_press=self.pressed)
        self.add_widget(self.b2)

    def pressed(self, instance):
        #print("Pressed")
        #name = self.name.text
        print("Pressed")

    def pressed_time(self, instance):
        time_ms = current_time_milliseconds()
        print(calculate_time_difference(time_ms + 20,time_ms))
        time.sleep(0.1) 
        new_time_ms = current_time_milliseconds()
        print(calculate_time_difference(time_ms,new_time_ms))
class ButtonimagesApp(App):
    def build(self):
        return SessionLayout()

if __name__ == '__main__':
    app = ButtonimagesApp()
    app.run()
