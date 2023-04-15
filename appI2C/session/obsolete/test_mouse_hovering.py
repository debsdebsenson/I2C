from kivy.app import App
from kivy.core.window import Window
Window.minimum_width, Window.minimum_height = 800, 600
from kivy.clock import Clock
from kivy.compat import string_types
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<ToolTipSpinner>:
<Tooltip>:
    size_hint: None, None
    size: self.texture_size[0]+5, self.texture_size[1]+5
    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            size: self.size
            pos: self.pos

<MyBar>:
    orientation: 'horizontal'
    padding: 2
    spacing: 2
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            width: 1.
            rectangle: (self.x+1, self.y-1, self.width, self.height)
    BoxLayout:
        orientation: 'horizontal'
        padding: 2,2,2,2
        spacing: 2
        size_hint: None, 1
        width: 110
        ToolTipSpinner:
            id:  _spinner_type_1
            tooltip_txt: 'Tooltip T1'
            text:  'Type 1'
            values:   ['0', '1', '2', '3']
            size_hint:  None, .45
            on_text:  self.on_spinner_select(self.text)
        ToolTipSpinner:
            id:  _spinner_type_2
            tooltip_txt: 'Tooltip T2\\nwith newline'
            text:  'Type 2'
            values:   ['4', '5', '6', '7', '8', '9']
            size_hint:  None, .45
            on_text:  self.on_spinner_select(self.text)
""")


class Tooltip(Label):
    pass


class MyBar(BoxLayout):
    pass


class ToolTipSpinner(Spinner):
    tooltip_txt = StringProperty('')
    tooltip_cls = ObjectProperty(Tooltip)
    
    def __init__(self, **kwargs):
        self._tooltip = None
        super(ToolTipSpinner, self).__init__(**kwargs)
        fbind = self.fbind
        fbind('tooltip_cls', self._build_tooltip)
        fbind('tooltip_txt', self._update_tooltip)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self._build_tooltip()
    
    def _build_tooltip(self, *largs):
        if self._tooltip:
            self._tooltip = None
        cls = self.tooltip_cls
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        self._tooltip = cls()
        self._update_tooltip()
    
    def _update_tooltip(self, *largs):
        txt = self.tooltip_txt
        if txt:
            self._tooltip.text = txt
        else:
            self._tooltip.text = ''
    
    def on_spinner_select(self, text):
        print(text)
    
    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        self._tooltip.pos = pos
        Clock.unschedule(self.display_tooltip) # cancel scheduled event since I moved the cursor
        self.close_tooltip() # close if it's opened
        if self.collide_point(*self.to_widget(*pos)):
            Clock.schedule_once(self.display_tooltip, 1)

    def close_tooltip(self, *args):
        Window.remove_widget(self._tooltip)

    def display_tooltip(self, *args):
        Window.add_widget(self._tooltip)
        
        
class MainApp(App):
    def build(self):
        return MyBar()

if __name__ == '__main__':
    MainApp().run()