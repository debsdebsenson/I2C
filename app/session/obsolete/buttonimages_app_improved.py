from kivy.app import App
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window

class SessionLayout(BoxLayout):
    # Constructor which takes x keyword arguments as input.
    def __init__(self, **kwargs):
        super(SessionLayout, self).__init__(**kwargs)

        layout = BoxLayout()
        image1 = Image(source='../images/placeholder3.JPG')
        image2 = Image(source='../images/placeholder2.JPG')
        layout.add_widget(image1)
        layout.add_widget(image2)
        Window.bind(on_keyboard=self.on_keyboard)

    def on_keyboard(self, window, key, *args):
        if key == 27: # ESC key code
            App.get_running_app().stop()

class ButtonimagesApp(App):
    def build(self):
        return SessionLayout()

if __name__ == "__main__":
    app = ButtonimagesApp()
    app.run()
