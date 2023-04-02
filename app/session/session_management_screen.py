from kivy.uix.boxlayout import BoxLayout

from scrollable_field import ScrollableField
 
 # Management of the screens
class SessionManagement(BoxLayout):
    def __init__(self, **var_args):
        super(SessionManagement, self).__init__(**var_args)

        self.cols = 1
        
        # TBD how to start next screen from here?
        self.scrollable_field_screen = ScrollableField()
        self.add_widget(self.scrollable_field_screen)