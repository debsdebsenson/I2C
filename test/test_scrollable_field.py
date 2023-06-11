import pytest
from kivy.clock import Clock
from appI2C.session.scrollable_field import ScrollableField # type: ignore


@pytest.fixture
def scrollable_field():
    # Create an instance of the ScrollableField class
    return ScrollableField()

def test_create_session(scrollable_field):
    # Simulate creating a session by calling the create_session method with input field text
    scrollable_field.create_session(scrollable_field.input_field, scrollable_field.scroll_layout, scrollable_field.session_label)

    # Check if the session row is added to the scroll layout
    assert len(scrollable_field.scroll_layout.children) == 1

"""
def test_delete_session_in_overview_screen(scrollable_field):
    # Add a session row to the scroll layout
    row_layout = BoxLayout()
    scrollable_field.scroll_layout.add_widget(row_layout)

    # Simulate deleting a session by calling the delete_session_in_overview_screen method
    scrollable_field.delete_session_in_overview_screen(row_layout, "session_name")

    # Check if the session row is removed from the scroll layout
    assert len(scrollable_field.scroll_layout.children) == 0

def test_confirmed_deletion_of_session_in_overview_screen(scrollable_field):
    # Add a session row to the scroll layout
    row_layout = BoxLayout()
    scrollable_field.scroll_layout.add_widget(row_layout)

    # Create a confirmation popup and simulate confirming the deletion
    confirm_popup = scrollable_field.delete_session_in_overview_screen(row_layout, "session_name")
    scrollable_field.confirmed_deletion_of_session_in_overview_screen(row_layout, confirm_popup, "session_name")

    # Check if the session row is removed from the scroll layout
    assert len(scrollable_field.scroll_layout.children) == 0

def test_clear_session_label(scrollable_field):
    # Set the session label text
    scrollable_field.session_label.text = "Session successfully created"

    # Schedule the clear_session_label method to be called after a delay
    Clock.schedule_once(scrollable_field.clear_session_label, 5)

    # Check if the session label text is cleared after the scheduled time
    assert scrollable_field.session_label.text == "" """
