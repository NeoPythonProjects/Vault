from kivy.app import App
from kivy.lang import Builder

from kivy.uix.recycleview import RecycleView

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

KV = """
ScreenManager
    padding: 10,10
    spacing: 10,10
    Screen
        name: 's1'
        BoxLayout
            Button
                text: 'go to screen 2'
                on_press: root.current = 's2'
            RV

    Screen
        name: 's2'
        BoxLayout
            Button
                text: 'go to screen 1'
                on_press: root.current = 's1'
            RV

<SelectableLabel>:
    background_color: 0.5,0.5,0.5,0.5

<RV>
    viewclass: 'SelectableLabel'
    RecycleBoxLayout
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
"""

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(10)]

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
  return super(TestScreen.SelectableLabel, self).refresh_view_attrs(
    rv, index, data)

def on_touch_down(self, touch):
  ''' Add selection on touch down '''
  try:
    if super(TestScreen.SelectableLabel, self).on_touch_down(touch):
      return True
    if self.collide_point(*touch.pos) and self.selectable:
      return self.parent.select_with_touch(self.index, touch)
  except:
      pass

def apply_selection(self, rv, index, is_selected):
  ''' Respond to the selection of items in the view. '''
  self.selected = is_selected
  if is_selected:
    print("selection changed to {0}".format(rv.data[index]))
    root.ids.output_label.text = str(rv.data[index])
    return str(rv.data[index])
  else:
    print("selection removed for {0}".format(rv.data[index]))



class MyApp(App):
    def build(self):
        self.root = Builder.load_string(KV)

MyApp().run()
