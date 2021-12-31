from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty

kv = """
<ScreenSelectButton>:
    on_release: self.switch_screen()

<DynamicScreen>
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: root.name
            font_size: 40
        Button:
            size_hint_y: None
            height: 48
            text: 'Go to Home Screen'
            on_release: root.manager.current = 'home'


<HomeScreen@Screen>:
    # no buttons here, that's done via screen manager
    # so RV doesn't get confused with gridlayout etc
    RV:                          # A Reycleview
        id: rv
        viewclass: 'ScreenSelectButton'  # The view class is defined above.
        data: self.rv_data_list  # the data is a list of dicts defined below in the RV class.
        scroll_type: ['bars', 'content']
        bar_width: 10
        RecycleBoxLayout:        
            # This layout is used to hold the Recycle widgets
            default_size: None, dp(48)   # This sets the height of the BoxLayout that holds a instance.
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height   # To scroll you need to set the layout height.
            orientation: 'vertical'


BoxLayout:
    orientation: 'vertical'
    Label:
        text: 'Using an RV list to create and change screens'
        size_hint_y: None
        height: 24
    # screenmanager within the boxlayout
    ScreenManager:
        id:sm
        HomeScreen:
            name: 'home'   
"""


class DynamicScreen(Screen):
    pass


class ScreenSelectButton(Button):
    def switch_screen(self):
        # check if screen exists, if it does not, create a screen.
        app = App.get_running_app()
        sm = app.root.ids.sm
        if sm.has_screen(self.text):
            sm.current = self.text
        else:
            # create screen, add to screen manager, and make it the current screen
            sm.add_widget(DynamicScreen(name=self.text))
            sm.current = self.text


class RV(RecycleView):
    rv_data_list = ListProperty()  # A list property is used to hold the data for the recycleview, see the kv code

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rv_data_list = [{'text': f'Screen {i}'} for i in range(1, 21)]
        # note: I am using the button labels as screen names


class SwitchCreateScreensApp(App):
    def build(self):
        return Builder.load_string(kv)


SwitchCreateScreensApp().run()


