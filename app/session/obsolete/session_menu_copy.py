# Kivy modules imports
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.clock import Clock

# Internal imports
from session_management_screen import SessionManagement


# This class sets up the layout of the first screen with two buttons and
# handles the button press events to switch to the next screen or close the
# application.
class  SessionMenu(FloatLayout):
    def __init__(self, **kwargs):
        super( SessionMenu, self).__init__(**kwargs)

        # Define buttons
        self.btn1 = Button(text='Start Session')
        self.btn2 = Button(text='Edit')
        self.btn3 = Button(text='Go back')

        # Set the size and position of the buttons
        self.btn1.size_hint = (0.5, 0.3)
        self.btn1.pos_hint = {'center_x': 0.5, 'center_y': 0.8}
        self.btn2.size_hint = (0.5, 0.3)
        self.btn2.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.btn3.size_hint = (0.5, 0.3)
        self.btn3.pos_hint = {'center_x': 0.5, 'center_y': 0.2}

        # bind button callbacks
        self.btn1.bind(on_press=self.edit_session)
        #self.btn1.bind(on_press=self.btn1_behaviour)
        self.btn2.bind(on_press=self.edit_session)
        self.btn3.bind(on_press=self.go_back_to_scrollable_field)

        # Add the buttons to the layout
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)

    def edit_session(self):
        print("This will be implemented in the future")

    def go_back_to_scrollable_field(self):
        print("This will be implemented in the future")

    # Implementation of a little delay before opening the next page 
    def btn1_behaviour(self, *args):

        # Clock.schedule_once(<action>, <delay time in s>)
        Clock.schedule_once(self.switch_to_next_view, 0.1)

    # Switch to the next screen view/page
    def switch_to_next_view(self, *args):
        app.screen_manager.current = 'sessionManagement'


class TestApp(App):
    self.start_screen = SessionMenu()


# Main function
if __name__ == '__main__':
    app = TestApp()
    app.run()