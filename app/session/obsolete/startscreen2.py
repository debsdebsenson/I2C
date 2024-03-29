import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, Screen

from app.session.session_management_screen import SessionManagement
from main import SwitchScreen


class  StartScreen(FloatLayout):
    def __init__(self, **kwargs):
        super( StartScreen, self).__init__(**kwargs)

        # Define buttons
        self.btn1 = Button(text='Select a session')
        """ self.btn1 = Button(text='Eintreten',
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#33cccc',
                                      background_normal='') """
        self.btn2 = Button(text='Close application')

        # Set the size and position of the buttons
        self.btn1.size_hint = (0.5, 0.3)
        self.btn1.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        self.btn2.size_hint = (0.5, 0.3)
        self.btn2.pos_hint = {'center_x': 0.5, 'center_y': 0.3}

        # bind button callbacks
        #self.btn1.bind(on_press=self.show_image)
        self.btn1.bind(on_press=self.btn1_behaviour)
        self.btn2.bind(on_press=self.close_app)

        # Add the buttons to the layout
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)


    # TBD: Here another menu is to be set up where the sessions can be selected
    """ def show_image(self, instance):
        self.clear_widgets()
        self.add_widget(Image(source="../images/placeholder1.png", size_hint=(1, 1))) """

    def btn1_behaviour(self, *args):
        #self.greeting.text = 'Herzlich Willkommen.'
        Clock.schedule_once(self.switch_to_next_view, 1)

    def switch_to_next_view(self, *args):
        app.screen_manager.current = 'sessionManagement'

    # Close the app
    def close_app(self, instance):
        App.get_running_app().stop()


""" class I2CApp(App):
    def build(self):
        return  StartScreen() """


""" if __name__ == '__main__':
    I2CApp().run() """