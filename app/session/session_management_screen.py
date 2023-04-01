from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
 
 # TBD: So far this is just a placeholder function for the actual screen
 # management class
class SessionManagement(GridLayout):
    def __init__(self, **var_args):
        super(SessionManagement, self).__init__(**var_args)

        self.cols = 1

        # Here the scrollable_field will be called at the end
        self.add_widget(Label(text='Hello World'))