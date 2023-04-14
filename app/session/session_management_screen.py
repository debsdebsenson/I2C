from kivy.uix.boxlayout import BoxLayout

from scrollable_field import ScrollableField
 
 # Management of the screens
class SessionManagementScrollableField(BoxLayout):
    def __init__(self, **var_args):
        super(SessionManagementScrollableField, self).__init__(**var_args)

        self.cols = 1
        
        self.scrollable_field_screen = ScrollableField()
        self.add_widget(self.scrollable_field_screen)