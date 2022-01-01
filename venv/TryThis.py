from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty
from kivy.uix.label import Label
from mysqldb import get_pw_from_record
from decorators import execute_sql


class HomeScreen(Screen):
    pass

class DynamicScreen(Screen):
    pass

class OutputScreen(Screen):
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

    def switch_to_confirmation_screen(self):
        #this class is a button, not the screen manager, so doesn't know these objects
        app = App.get_running_app()
        sm = app.root.ids.sm
        # screen is built at inception, so is not updated for latest entry in selection.txt
        sm.get_screen('confirmation_screen').ids.output_label.text = self.text
        sm.current = 'confirmation_screen'
        return None


class RV(RecycleView):
    rv_data_list = ListProperty()  # A list property is used to hold the data for the recycleview, see the kv code

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rv_data_list = [{'text': f"App: {x[0]} - User: {x[1]}"} for x in self.get_data()]#[{'text': f'Screen {i}'} for i in range(1, 21)]
        # note: I am using the button labels as screen names

    @staticmethod
    @execute_sql('runquery')
    def get_data_cursor():
      sqlstr = """
      SELECT application, app_user_id
      FROM applications
      """
      return sqlstr


    def get_data(self):
      self.rv_data_list = self. get_data_cursor()
      print(self.rv_data_list)
      return self.rv_data_list


class ConfirmSelectionLabel(Label):
    pass


class ConfirmationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class WrongSelectionButton(Button):
    @staticmethod
    def switch_back_to_selection_screen():
        app = App.get_running_app()
        sm = app.root.ids.sm
        #App.get_screen(sm.current).stop()
        sm.current = 'selection_screen'


class ConfirmSelectionButton(Button):
    def switch_to_output_screen(self):
        # this class is a button, not the screen manager, so doesn't know these objects
        app = App.get_running_app()
        sm = app.root.ids.sm
        # read selection
        selection =sm.get_screen('confirmation_screen').ids.output_label.text
        # split into App and UserID:
        app, userid = selection.split("-")
        app = app[5:].strip()
        print(app, len(app))
        userid = userid[7:].strip()
        print(userid, len(userid))
        # get the password
        pw = get_pw_from_record('NeoPythonProjects', app)
        # 3. empty the file that held the key

        #pw = 'test pw for now which is really long to see whehter wrapping works'
        sm.get_screen('output_screen').ids.output_label_userid.text = userid
        sm.get_screen('output_screen').ids.output_label_app.text = app
        sm.get_screen('output_screen').ids.output_label_pw.text = pw
        sm.current = 'output_screen'
        return None


class SwitchCreateScreensApp(App):
    def build(self):
        return Builder.load_file('TryThis.kv')


if __name__ == "__main__":
    SwitchCreateScreensApp().run()


