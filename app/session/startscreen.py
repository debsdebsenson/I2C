# events: https://kivy.org/doc/stable/guide/events.html

# import kivy module
# import kivy

from kivy.app import App


from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

# BoxLayout arranges children in a vertical or horizontal box.
# or help to put the children at the desired location.
# from kivy.uix.boxlayout import BoxLayout

from eye_detection import current_time_milliseconds

# from eye_detection import calculate_time_difference

import pyautogui

import time

"""
from eye_detection import start_camera_session
from eye_detection import main_eye_detection
from eye_detection import finish_webcam_session """


class StartScreenLayout(GridLayout):
    # Constructor which takes x keyword arguments as input.
    def __init__(self, **kwargs):
        # This is how an event can be triggered
        self.register_event_type("on_test")

        super(StartScreenLayout, self).__init__(**kwargs)
        self.cols = 1

        self.b1 = Button(
            text="Wanna Start?",
            color=(1, 0, 0.65, 1),
            size_hint=(0.49, 0.49),
            pos_hint={"left": 1, "center_y": 0.5},
        )

        # Add an event when this button is pressed
        self.b1.bind(on_press=self.pressed_button)
        self.add_widget(self.b1)

        """     def click_on_selected_image():
        screen_size = pyautogui.size()
        screen_size_x = screen_size[0]
        screen_size_y = screen_size[1]

        click_point_y = int(screen_size_y / 2)
        click_point_x = int(screen_size_x / 2)
        click_point = (click_point_x, click_point_y)
        print(f"Calculated click point (x, y): {click_point}") """

    def pressed_button(self, instance):
        print("Button Pressed")

    def calc_click_point(self):
        screen_size = pyautogui.size()
        # print(screen_size)
        screen_size_x = screen_size[0]
        screen_size_y = screen_size[1]

        click_point_y = int(screen_size_y / 2)
        click_point_x = int(screen_size_x / 2)
        click_point = (click_point_x, click_point_y)
        print(f"Calculated click point (x, y): {click_point}")
        return click_point

    def do_something(self):
        # when do_something is called, the 'on_test' event will be
        # dispatched with the value
        # self.dispatch('on_test')
        click_point = self.calc_click_point()
        # time.sleep(10)
        # pyautogui.click(click_point)
        print(click_point)

    def on_test(self, *args):
        # print("I am dispatched", args)
        print("____________________________")
        print(current_time_milliseconds())
        time.sleep(0.1)
        print(current_time_milliseconds())
        print("____________________________")

    def my_callback(self, instance):
        print("Hello, I got an event!")
        # instance.pressed_start


class StartScreenApp(App):
    def build(self):
        ev = StartScreenLayout()

        # Binds on_test method and my_callback method together
        # ev.bind(on_test=ev.my_callback)

        # just call any method on the ev object
        ev.do_something()
        return ev


if __name__ == "__main__":
    app = StartScreenApp()
    app.run()
