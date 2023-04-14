from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MyPopup(Popup):
    pass

class MyButton(Button):
    def on_press(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Do you want to proceed?'))
        button_layout = BoxLayout()
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content.add_widget(button_layout)
        popup = MyPopup(title='Confirmation', content=content, size_hint=(None, None), size=(400, 200))
        yes_button.bind(on_release=popup.dismiss)
        no_button.bind(on_release=popup.dismiss)
        popup.open()

class MyApp(App):
    def build(self):
        return MyButton(text='Open Popup')

if __name__ == '__main__':
    MyApp().run()
