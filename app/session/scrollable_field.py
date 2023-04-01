from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivy.storage.jsonstore import JsonStore
# import json

class ScrollableFieldApp(App):
    
    def build(self):
        # Create the main layout of the app
        layout = BoxLayout(orientation='vertical')
        
        # Create the scrollable field and add it to the layout
        scroll_view = ScrollView()
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        scroll_view.add_widget(scroll_layout)
        layout.add_widget(scroll_view)

        # TBD: Load the session_data from the JSON file and create the placeholder text labels and delete buttons
        # + if this file does not exist throw error (try catch block)
        session_data_json = JsonStore('./app/session/data.json')
        print("_______________________________")
        self.print_session_data_from_json(session_data_json, 'Session 1', 'date')
        print("_______________________________")
        
        for text in session_data_json:
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
            row_layout.add_widget(Label(text=text))
            row_layout.add_widget(Button(text="Delete", on_press=self.delete_row))
            scroll_layout.add_widget(row_layout)
        
        """         # Create some placeholder text labels and delete buttons
        for i in range(20):
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
            row_layout.add_widget(Label(text=f"Row {i+1}"))
            row_layout.add_widget(Button(text="Delete", on_press=self.delete_row))
            scroll_layout.add_widget(row_layout) """
        
        # Create the input field and the "create" button
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        input_field = TextInput(multiline=False)
        input_layout.add_widget(input_field)
        input_layout.add_widget(Button(text="Create", on_press=lambda x: self.create_row(input_field, scroll_layout)))
        layout.add_widget(input_layout)
        
        # Create the label for displaying session name creation
        self.session_label = Label(text="", color=[1, 0, 0, 1], size_hint=[None, None], size=[300, 50], pos=[800, 550])
        layout.add_widget(self.session_label)
        
        return layout
    
    # Methos for printing specific sesion data
    # TBD: this method is mainly for debugging, can be deleted later
    def print_session_data_from_json(self, session_data_json, session_name, parameter_to_be_printed):
        print(f'Parameter "{parameter_to_be_printed}" of Session "{session_name}" is:', session_data_json.get(session_name)[parameter_to_be_printed])

    # TBD: Method for Adding Sessions to the data.json file
    #def add_session_data_to_json(self, session_data_json, session_information):
    
    # TBD: Method for renaiming sessions

    def delete_row(self, instance):
        # TBD: Write some text to the confirm deletion box
        # Ask for confirmation before deleting the row
        confirm_popup = Popup(title='Confirm Deletion',
                              content=BoxLayout(orientation='horizontal', size_hint_y=None, height=40),
                              size_hint=(None, None), size=(400, 200))
        yes_button = Button(text="Yes", on_press=lambda x: self.delete_row_confirmed(instance.parent, confirm_popup))
        no_button = Button(text="No", on_press=confirm_popup.dismiss)
        confirm_popup.content.add_widget(yes_button)
        confirm_popup.content.add_widget(no_button)
        confirm_popup.open()

    def delete_row_confirmed(self, row_layout, confirm_popup):
        # Remove the row containing the delete button that was pressed
        scroll_layout = row_layout.parent
        scroll_layout.remove_widget(row_layout)
        confirm_popup.dismiss()
    
    def create_row(self, input_field, scroll_layout):
        # Create a new row with the text from the input field and add it to the scrollable field
        text = input_field.text

        # Clear the input field after creating the new row
        input_field.text = ''
        row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        row_layout.add_widget(Label(text=text))
        row_layout.add_widget(Button(text="Delete", on_press=self.delete_row))
        scroll_layout.add_widget(row_layout)
        
        # Display the session creation confirmation message for 5 seconds
        self.session_label.text = f"Session {text} successfully created"
        Clock.schedule_once(self.clear_session_label, 5)
    
    def clear_session_label(self, dt):
        self.session_label.text = ""

if __name__ == '__main__':
    ScrollableFieldApp().run()