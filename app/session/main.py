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

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.clock import Clock

from session_management_screen import SessionManagement

class  StartScreen(FloatLayout):
    def __init__(self, **kwargs):
        super( StartScreen, self).__init__(**kwargs)

        # Define buttons
        self.btn1 = Button(text='Select a session')
        self.btn2 = Button(text='Close application')

        # Set the size and position of the buttons
        self.btn1.size_hint = (0.5, 0.3)
        self.btn1.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        self.btn2.size_hint = (0.5, 0.3)
        self.btn2.pos_hint = {'center_x': 0.5, 'center_y': 0.3}

        # bind button callbacks
        self.btn1.bind(on_press=self.btn1_behaviour)
        self.btn2.bind(on_press=self.close_app)

        # Add the buttons to the layout
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)

    def btn1_behaviour(self, *args):
        # Clock.schedule_once(<action>, <delay time in s>)
        Clock.schedule_once(self.switch_to_next_view, 0.1)

    def switch_to_next_view(self, *args):
        app.screen_manager.current = 'sessionManagement'

    # Close the app
    def close_app(self, instance):
        App.get_running_app().stop()

class I2CApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.start_screen = StartScreen()
        screen = Screen(name='startScreen')
        screen.add_widget(self.start_screen)
        self.screen_manager.add_widget(screen)

        self.session_management = SessionManagement()
        screen = Screen(name='sessionManagement')
        screen.add_widget(self.session_management)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    app = I2CApp()
    app.run()
