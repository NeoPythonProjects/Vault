from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from os.path import sep, expanduser, isdir, dirname
from kivy_garden.filebrowser import FileBrowser
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.recycleview import RecycleView
# Program to explain how to use recycleview in kivy

# import the kivy module
from kivy.app import App

# The ScrollView widget provides a scrollable view
from kivy.uix.recycleview import RecycleView

Builder.load_file('test_gui_2.kv')

class TestScreen(Screen):
    pass

# Define the Recycleview class which is created in .kv file
class ExampleViewer(RecycleView):
    def __init__(self, **kwargs):
        super(ExampleViewer, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(20)]


# Create the App class with name of your app.
class SampleApp(App):
    def build(self):
        return RootWidget()
        #return TestScreen()
        #return ExampleViewer()

def run_example_viewer():
    # run the App
    SampleApp().run()

class RootWidget(ScreenManager):
  pass

SampleApp().run()