import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock


class SessionMenuRegular(FloatLayout):
    def __init__(self, **kwargs):
        super(SessionMenuRegular, self).__init__(**kwargs)

        # Define buttons
        self.btn1 = Button(text='Start Session')
        self.btn2 = Button(text='Edit')
        self.btn3 = Button(text='Go back')

        # Set the size and position of the buttons
        self.btn1.size_hint = (0.5, 0.15)
        self.btn1.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        self.btn2.size_hint = (0.5, 0.15)
        self.btn2.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.btn3.size_hint = (0.5, 0.15)
        self.btn3.pos_hint = {'center_x': 0.5, 'center_y': 0.3}

        self.btn1.bind(on_press=lambda instance: self.start_session())
        self.btn2.bind(on_press=lambda instance: self.edit_session())
        self.btn3.bind(on_press=lambda instance: self.go_back_to_scrollable_field())

        # Add the buttons to the layout
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)

    def this_is_for_testing_initially():
        raise SystemExit (1)

    def edit_session(self):
        print("Editing sessions will be implemented in the future")

    def go_back_to_scrollable_field(self):
        print("Going back to last screen will be implemented in the future")

    # Implementation of a little delay before opening the next page 
    def start_session(self, *args):

        # Clock.schedule_once(<action>, <delay time in s>)
        Clock.schedule_once(self.switch_to_next_view, 0.1)

    # Switch to the next screen view/page
    def switch_to_next_view(self, *args):
        #app.screen_manager.current = 'sessionManagement'
        print("Placeholder")


class SessionMenuEmptySession(FloatLayout):
    def __init__(self, **kwargs):
        super(SessionMenuEmptySession, self).__init__(**kwargs)

        # Define buttons
        self.btn1 = Button(text='Design my Session')
        self.btn2 = Button(text='Go back')

        # Set the size and position of the buttons
        self.btn1.size_hint = (0.5, 0.15)
        self.btn1.pos_hint = {'center_x': 0.5, 'center_y': 0.6}
        self.btn2.size_hint = (0.5, 0.15)
        self.btn2.pos_hint = {'center_x': 0.5, 'center_y': 0.4}

        self.btn1.bind(on_press=lambda instance: self.switch_to_edit_session())
        self.btn2.bind(on_press=lambda instance: self.go_back_to_scrollable_field())

        # Add the buttons to the layout
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)

    def go_back_to_scrollable_field(self):
        print("Going back to last screen will be implemented in the future")

    # Switch to the next screen view/page
    def switch_to_edit_session(self, *args):
        #app.screen_manager.current = 'sessionManagement'
        print("Placeholder")
        # Clock.schedule_once(<action>, <delay time in s>)
        #Clock.schedule_once(self.switch_to_next_view, 0.1)


class MyApp(App):
    def build(self):
        return SessionMenuEmptySession()


if __name__ == '__main__':
    MyApp().run()
