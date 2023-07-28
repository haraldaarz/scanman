import sys
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk


class MyApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyGtkApplication")
        GLib.set_application_name("My Gtk Application")

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self, title="Hello World")
        
        button = Gtk.Button(label="Click Me!") # Create a button
        button.connect("clicked", self.on_button_clicked) # Connect a callback function to the button's "clicked" signal
        window.set_child(button)  # Set the button as the child of the window

        window.show() # Show the window and its child widget

    def on_button_clicked(self, button):
        print("Button clicked!")


app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
