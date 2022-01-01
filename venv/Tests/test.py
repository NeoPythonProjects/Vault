from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from os.path import sep, expanduser, isdir, dirname
from kivy_garden.filebrowser import FileBrowser
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.recycleview import RecycleView

from decorators import execute_sql


Builder.load_file('test_gui.kv')


class TestScreen(Screen):

  class MyLayout(BoxLayout):
    rows = [("application", "app_user_id")]

    @execute_sql('runquery')
    def get_data_cursor():
      sqlstr = """
      SELECT application, app_user_id
      FROM applications
      """
      return sqlstr


    def get_data(self, root):
      self.rows = root.MyLayout.get_data_cursor()
      print(root.ids)
      print(self.rows)
      root.ids.output_label.text="\n".join([str(x) for x in self.rows])
      #TODO: can we run non-screen kv file from separate py file in bring across the results?



class MainApp(App):
  def build(self):
    return RootWidget()

class RootWidget(ScreenManager):
  pass


if __name__ == "__main__":
  pass
  MainApp().run()