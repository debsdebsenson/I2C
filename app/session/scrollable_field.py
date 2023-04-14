"""
Here you find the code for the second screen, the menu where Sessions can be
started, created and deleted from.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder

from datetime import datetime

import json

# information about kivy.storage: https://kivy.org/doc/stable/api-kivy.storage.html#module-kivy.storage
from kivy.storage.jsonstore import JsonStore

JSON_FILEPATH='./app/session/data.json'
PRETTY_JSON_FILEPATH='./app/session/data_pretty.json'

class MyPopup(Popup):
    pass

class ScrollableField(BoxLayout):
    
    def __init__(self, **var_args):
        super(ScrollableField, self).__init__(**var_args)

        self.cols = 1

        # Create the scrollable field and add it to the layout
        scroll_view = ScrollView(scroll_type=['bars'], bar_width=10)
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        scroll_view.add_widget(scroll_layout)
        self.add_widget(scroll_view)

        # TBD: try catch - on all critical methods and calls of methods
        session_data_json = self.load_data_from_json()
        
        for text in session_data_json:
            session_name=text
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
            row_layout.add_widget(Button(text=text, background_color=[0, 0, 0, 0], on_press=lambda instance: self.go_to_session_menu()))
            row_layout.add_widget(Button(text="Delete", on_press=lambda instance: self.delete_session_in_overview_screen(instance, session_name)))
            scroll_layout.add_widget(row_layout)

        # Create the label for displaying session name creation
        layout = BoxLayout(orientation='vertical')
        self.session_label = Label(text="", color=[1, 0, 0, 1], size_hint=[None, None], size=[300, 50], pos=[800, 550])
        layout.add_widget(self.session_label)
        self.add_widget(layout)

        # Create the input field and the "Create" button
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)

        input_field = TextInput(multiline=False)
        input_field.bind(on_text_validate=lambda x: self.on_enter(input_field, scroll_layout, self.session_label))

        input_layout.add_widget(input_field)
        create_button=Button(text="Create", on_press=lambda x: self.create_session(input_field, scroll_layout, self.session_label))
        input_layout.add_widget(create_button)
        self.add_widget(input_layout)

    """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Go to session menu
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

    # In this function a switch to the session menu is triggered
    # TBD: how can this be implemented with the screen manager???
    def go_to_session_menu(self):
        print("Placeholder - from here change to the session menu")

    """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    JSON connected methods
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

    # Loade all data from a JSON file
    def load_data_from_json(self):
        session_data_json = JsonStore(JSON_FILEPATH)
        return session_data_json
    
    # This method is mainly used for faciliating the develpment process by
    # restructuring the content of a JSON file nicely and more readable.
    #def pretty_restructuring_json_content(self, data_to_be_restructured):
    def pretty_restructuring_json_content(self):
        with open(JSON_FILEPATH, 'r') as json_file:
            data = json.load(json_file)

        with open(PRETTY_JSON_FILEPATH, 'w') as pretty_file:
            json.dump(data, pretty_file, indent=4)

    # Method for printing specific sesion data
    # This method is mainly for debugging, can be deleted later
    def print_session_data_from_json(self, session_data_json, session_name, parameter_to_be_printed):
        print(f'Parameter "{parameter_to_be_printed}" of Session "{session_name}" is:', session_data_json.get(session_name)[parameter_to_be_printed])

    # Method for Adding Sessions to the data.json file
    # session_information is a list, the second parameter is also a list
    def add_session_data_to_json(self, session_data_json, session_information):
        #These are single parameters
        session_name = session_information[0]
        date_data= session_information[2]
        # This is a list
        empty_list = session_information[1]

        session_data_json.put(session_name, image_pathes=empty_list, date=date_data)
    
    # Method for removing entries from the json file
    def remove_session_data_from_json(self, session_data_json, name_of_del_session):
        if session_data_json.exists(name_of_del_session):
            print(f'Remove session "{name_of_del_session}" with entries:', session_data_json.get(name_of_del_session))
            session_data_json.delete(name_of_del_session)

    # Method for finding an entry
    """ # or guess the key/entry for a part of the key
    def find_session_key_from_json(self, session_data_json, input_to_search_for):
        for item in store.find(name='Gabriel'):
            print('tshirtmans index key is', item[0])
            print('his key value pairs are', str(item[1])) """
    """
    # or something like this:
    if store.exists('tito'):
    print('tite exists:', store.get('tito'))
    store.delete('tito')
    """

    """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Functionality within screens
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

    # Popup window for confirming before deleting the Session 
    def delete_session_in_overview_screen(self, instance, name_of_del_session):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Are you sure you want to delete the session?'))
        button_layout = BoxLayout()
        yes_button = Button(text="Yes", on_press=lambda x: self.confiremd_deletion_of_session_in_overview_screen(instance.parent, confirm_popup, name_of_del_session))
        no_button = Button(text='No')
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content.add_widget(button_layout)
        confirm_popup = Popup(title='Confirmation', content=content, size_hint=(None, None), size=(400, 200))
        yes_button.bind(on_release=confirm_popup.dismiss)
        no_button.bind(on_release=confirm_popup.dismiss)
        confirm_popup.open()

    def confiremd_deletion_of_session_in_overview_screen(self, row_layout, confirm_popup, name_of_del_session):
        # Remove the row containing the delete button that was pressed
        scroll_layout = row_layout.parent
        scroll_layout.remove_widget(row_layout)
        
        # Remove session from JSON file
        session_data_json = self.load_data_from_json()
        self.remove_session_data_from_json(session_data_json, name_of_del_session)

        confirm_popup.dismiss()
    
    # Call the method to create a session when the ENTER key is pressed
    def on_enter(instance, input_field, scroll_layout, session_label):
        instance.create_session(input_field, scroll_layout, session_label)

    # Create a session
    def create_session(self, input_field, scroll_layout, session_label):
        # Get the text from the input field
        text = input_field.text.strip()

        # Only add the text if it is not empty
        if text:
            # Clear the input field after creating the new row
            input_field.text = ''
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
            row_layout.add_widget(Label(text=text))
            row_layout.add_widget(Button(text="Delete", on_press=lambda instance: self.delete_session_in_overview_screen(instance, session_name)))
            scroll_layout.add_widget(row_layout)

            # Add session to JSON storage file
            session_information=[]
            session_data_json = self.load_data_from_json()
            date_data = datetime.today().strftime('%Y-%m-%d')
            empty_list=[]
            session_name=text
            session_information = [session_name, empty_list, date_data]
            self.add_session_data_to_json(session_data_json, session_information)

            # Increasing readability of JSON file: output = data_pretty.json
            self.pretty_restructuring_json_content()
            
            # Display the session creation confirmation message for 5 seconds
            session_label.text = f"Session {text} successfully created"
            Clock.schedule_once(self.clear_session_label, 5)
    
    def clear_session_label(self, dt):
        self.session_label.text = ""


"""
# TBD: think about this!: Should this be implemented to be called within the sessions itself or also on the scrollable field?

    # TBD: Finish method for renaiming sessions - not yet working as intended,
    # very static - it seems like there is no possibility to change entries
    # implemented in kivy
    def rename_session_data_in_json(self, session_data_json, session_information):
        # Unpack data from session_information list
        session_name = session_information[0]
        parameter_to_be_changed = session_information[1]
        new_session_data_value = session_information[2]
        if session_data_json.exists(session_name): #& session_data_json.exists(parameter_to_be_changed):
            print(f'Rename parameter in session "{session_name}". Change "{parameter_to_be_changed}" from {session_data_json.get(session_name)[parameter_to_be_changed]} to "{new_session_data_value}".')
            session_data_json.put(session_name, date=new_session_data_value)
"""