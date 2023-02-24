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

# This layout allows you to set relative coordinates for children.
from kivy.uix.relativelayout import RelativeLayout

# BoxLayout arranges children in a vertical or horizontal box.
# or help to put the children at the desired location.
from kivy.uix.boxlayout import BoxLayout

# creating the root widget used in .kv file
class Buttonimages(BoxLayout):
    '''
        no need to do anything here as
        we are building things in .kv file
    '''
    pass

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

        return rl

if __name__ == '__main__':
    app = ButtonimagesApp()
    app.run()
