from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from os.path import sep, expanduser, isdir, dirname
from kivy_garden.filebrowser import FileBrowser
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from decorators import execute_sql

class ConfirmationScreen(Screen):
  pass
  with open('files/selection.txt','r') as f:
    data=f.read()
    f.close()

class ShowConfScreen(App):
  def build(self):
    Builder.load_file('selection_confirm.kv')
    return RootWidget()

class RootWidget(ScreenManager):
  pass

if __name__=="__main__":
  ShowConfScreen().run()