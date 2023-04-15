from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

class SessionLayout(GridLayout):
    # Constructor which takes x keyword arguments as input.
    def __init__(self, **kwargs):
        super(SessionLayout, self).__init__(**kwargs)
        self.cols = 2

        self.img1 = Image(source ='../images/placeholder3.JPG')
        self.add_widget(self.img1)

        self.img2 = Image(source ='../images/placeholder2.JPG')
        self.add_widget(self.img2)

class ButtonimagesApp(App):
    def build(self):
        return SessionLayout()


if __name__ == "__main__":
    app = ButtonimagesApp()
    app.run()
