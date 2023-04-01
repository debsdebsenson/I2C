from kivy.uix.boxlayout import BoxLayout

from scrollable_field import ScrollableField
 
 # TBD: So far this is just a placeholder function for the actual screen
 # management class
class SessionManagement(BoxLayout):
    def __init__(self, **var_args):
        super(SessionManagement, self).__init__(**var_args)

        self.cols = 1

        # Here the scrollable_field will be called at the end
        #self.add_widget(Label(text='Hello World'))
        
        # TBD: find solution to insert this screen here! - 1. implement minimal example, 2. expand it until it is working
        self.scrollable_field_screen = ScrollableField()
        self.add_widget(self.scrollable_field_screen)