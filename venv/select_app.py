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
from kivy.uix.button import Button
from selection_confirm import ShowConfScreen

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
  ''' Adds selection and focus behaviour to the view. '''
  pass


class SelectableLabel(RecycleDataViewBehavior, Label):
  ''' Add selection support to the Label '''
  index = None
  selected = BooleanProperty(False)
  selectable = BooleanProperty(True)

  def refresh_view_attrs(self, rv, index, data):
    ''' Catch and handle the view changes '''
    self.index = index
    return super(SelectableLabel, self).refresh_view_attrs(
      rv, index, data)

  def on_touch_down(self, touch):
    ''' Add selection on touch down '''
    if super(SelectableLabel, self).on_touch_down(touch):
      return True
    if self.collide_point(*touch.pos) and self.selectable:
      return self.parent.select_with_touch(self.index, touch)

  def apply_selection(self, rv, index, is_selected):
    ''' Respond to the selection of items in the view. '''
    self.selected = is_selected
    if is_selected:
      print("selection changed to {0}".format(rv.data[index]))
      #return 100#rv.data[index]
      #TODO: returning the value doesn't work
      # run code from here
      # maybe save selection to a file
      # trigger a SEPARATE screen wwith a lable showing selection and buttong to confirm and continue
      # trigger separate screen by using separate kv file and separate py file that you import into here

      #for this to work you need a screen manager
      # so all needs to be built into main.py
      self.manager.current = None
      with open('files/selection.txt','w') as f:
        f.write(str(rv.data[index]))
        f.close()
        ShowConfScreen().run()
    else:
      print("selection removed for {0}".format(rv.data[index]))


class ListView(RecycleView):
  def __init__(self, **kwargs):
    super(ListView, self).__init__(**kwargs)
    #self.data = [{'text':'123'},{'text':'fdsdfs'}]
    #self.data = []

  @execute_sql('runquery')
  def get_data_cursor():
    sqlstr = """
    SELECT application, app_user_id
    FROM applications
    """
    return sqlstr

  def get_data(self):
    #print(*args)
    print('triggered')
    self.data = ListView.get_data_cursor()
    #print(root.ids)
    print(self.data)
    return self.data



class MainApp(App):
  def build(self):
    root = Builder.load_file('select_app.kv')
    return ListView()


if __name__ == "__main__":
  pass
  MainApp().run()