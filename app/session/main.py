"""
Here a Kivy application with two screens managed by a ScreenManager is.

The first screen is called StartScreen and has two buttons: "Select a session"
and "Close application". When the "Select a session" button is pressed, it
calls the switch_to_next_view method, which switches the current screen to the
second screen, called SessionManagement, using the current attribute of the
ScreenManager. When the "Close application" button is pressed, it calls the
close_app method, which stops the Kivy application.
The second screen is called SessionManagement and is defined in a separate file
called "session_management_screen.py", which is imported at the beginning of
the code.
"""

# Kivy modules imports
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.lang import Builder

# Internal imports
from session_management_screen import SessionManagementScrollableField

# Load content (buttons and theit behaviour) the kv file
Builder.load_file('./kv_files/start_screen.kv')

# This class handles the button press events to switch to the next screen or
#  close the application for the start screen.
class  StartScreen(Screen):
#class  StartScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

    # Implementation of a little delay before opening the next page 
    def btn1_behaviour(self, *args):

        # Clock.schedule_once(<action>, <delay time in s>)
        Clock.schedule_once(self.switch_to_next_view, 0.1)

    # Switch to the next screen view/page
    def switch_to_next_view(self, *args):
        app.screen_manager.current = 'sessionManagement'

    # Close the app
    def close_app(self):
        App.get_running_app().stop()


class MyScreenManager(ScreenManager):
    pass

# The I2CApp class inherits from the App class in Kivy and is responsible for
# building and running the application.
class I2CApp(App):

    # The build function is responsible for setting up the user interface by
    # creating the ScreenManager and adding the necessary widgets to it, which
    # allows the user to interact with the application through the screens
    # defined in the StartScreen and SessionManagement classes.
    def build(self):
        self.screen_manager = MyScreenManager()
        self.screen_manager.add_widget(StartScreen(name="start_screen"))

        self.session_management = SessionManagementScrollableField()
        screen = Screen(name='sessionManagement')
        screen.add_widget(self.session_management)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

# Main function
if __name__ == '__main__':
    app = I2CApp()
    app.run()
