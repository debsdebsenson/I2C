""" 
Here you find the code for the second screen, the menu where Sessions can be
started, created and deleted from.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import os
import json
from kivy.storage.jsonstore import JsonStore

from session_menu import SessionMenuRegular

class MyPopup(Popup):
    pass

class MyScreenManager(ScreenManager):
    pass

class ScrollableField(BoxLayout):

    def __init__(self, **kwargs):
        super(ScrollableField, self).__init__(**kwargs)
        self.orientation = 'vertical'
        scroll_layout = self.create_scroll_layout()
        self.add_widget(self.create_scroll_view(scroll_layout))
        self.session_label = self.create_session_label()
        self.add_widget(self.create_input_layout(scroll_layout))
        self.add_widget(self.session_label)

    def create_scroll_layout(self):
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        session_data_json = self.load_data_from_json()
        for text in session_data_json:
            session_name = text
            row_layout = self.create_row_layout(session_name)
            scroll_layout.add_widget(row_layout)
        return scroll_layout

    def create_scroll_view(self, scroll_layout):
        scroll_view = ScrollView(scroll_type=['bars'], bar_width=10)
        scroll_view.add_widget(scroll_layout)
        return scroll_view

    def create_row_layout(self, session_name):
        row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        button1 = Button(text=session_name, background_color=[0, 0, 0, 0], on_press=self.go_to_session_menu)
        button2 = Button(text="Delete", on_press=lambda instance: self.delete_session_in_overview_screen(instance, session_name))
        row_layout.add_widget(button1)
        row_layout.add_widget(button2)
        return row_layout

    def create_session_label(self):
        layout = BoxLayout(orientation='vertical')
        session_label = Label(text="", color=[1, 0, 0, 1], size_hint=[None, None], size=[300, 50], pos=[800, 550])
        layout.add_widget(session_label)
        return layout

    def create_input_layout(self, scroll_layout):
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        input_field = TextInput(multiline=False)
        input_field.bind(on_text_validate=lambda x: self.on_enter(input_field, scroll_layout, self.session_label))
        create_button = Button(text="Create", on_press=lambda x: self.create_session(input_field, scroll_layout, self.session_label))
        input_layout.add_widget(input_field)
        input_layout.add_widget(create_button)
        return input_layout

    #####################################################################################################
    # Entrypoint to the session menu
    def go_to_session_menu(self, instance):
        print("Placeholder - from here change to the session menu")
        

    def load_data_from_json(self):
        session_data_json = JsonStore(self.get_json_filepath())
        return session_data_json
    
    def get_filepath_to_session_data(self):
        # This method concatenates and returns the absolute file path to the session_data folder
        abs_path_appI2C = os.path.join(os.path.abspath(os.getcwd()), 'appI2C')
        abs_path_session = os.path.join(abs_path_appI2C, 'session')
        abs_path_session_data = os.path.join(abs_path_session, 'sessions_data')
        return abs_path_session_data

    def get_json_filepath(self):
        # Returns the absolute file path of the JSON file.
        # Raises an exception if the file does not exist or is not a file.
        json_file = os.path.join(self.get_filepath_to_session_data(), 'data.json')
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"JSON file '{json_file}' does not exist.")
        elif not os.path.isfile(json_file):
            raise ValueError(f"JSON file '{json_file}' is not a file.")
        return json_file
    
    def create_session(self, input_field, scroll_layout, session_label):
        session_name = input_field.text
        if not session_name:
            return
        session_name = session_name.strip()
        session_data_json = self.load_data_from_json()
        if session_name in session_data_json:
            session_label.text = "Session name already exists!"
            return
        session_data_json[session_name] = {}
        row_layout = self.create_row_layout(session_name)
        scroll_layout.add_widget(row_layout)
        input_field.text = ""
        session_label.text = "Session created!"

    def save_data_to_json(self, data):
        json_file = self.get_json_filepath()
        with open(json_file, "w") as file:
            json.dump(dict(data), file)

    # Popup window for confirming before deleting the Session 
    def delete_session_in_overview_screen(self, instance, name_of_del_session):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Are you sure you want to delete the session?'))
        button_layout = BoxLayout()
        yes_button = Button(text="Yes", on_press=lambda x: self.confirmed_deletion_of_session_in_overview_screen(instance.parent, confirm_popup, name_of_del_session))
        no_button = Button(text='No')
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content.add_widget(button_layout)
        confirm_popup = Popup(title='Confirmation', content=content, size_hint=(None, None), size=(400, 200))
        yes_button.bind(on_release=confirm_popup.dismiss)
        no_button.bind(on_release=confirm_popup.dismiss)
        confirm_popup.open()

    # Method for removing entries from the json file
    def remove_session_data_from_json(self, session_data_json, name_of_del_session):
        if session_data_json.exists(name_of_del_session):
            print(f'Remove session "{name_of_del_session}" with entries:', session_data_json.get(name_of_del_session))
            session_data_json.delete(name_of_del_session)

    def confirmed_deletion_of_session_in_overview_screen(self, row_layout, confirm_popup, name_of_del_session):
        # Remove the row containing the delete button that was pressed
        scroll_layout = row_layout.parent
        scroll_layout.remove_widget(row_layout)
        
        # Remove session from JSON file
        session_data_json = self.load_data_from_json()
        self.remove_session_data_from_json(session_data_json, name_of_del_session)

        confirm_popup.dismiss()

""" # TBD: think about this!: Should this be implemented to be called within the sessions itself or also on the scrollable field?

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

 