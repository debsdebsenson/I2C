from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollableLabel, self).__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(50):
            layout.add_widget(Label(text=f"Label {i}", size_hint_y=None, height=40))

        self.add_widget(layout)

class MyApp(App):
    def build(self):
        return ScrollableLabel(scroll_type=['bars'], bar_width=10)

if __name__ == '__main__':
    MyApp().run()