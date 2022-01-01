from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from mysqldb import get_pw_from_record, get_vault_uid_from_record
from encryption import get_encryption_key, encrypt, decrypt
from login import encrypt_password
from decorators import execute_sql, logged_in

class LoginScreen(Screen):

  @logged_in
  def log_in(self, user: str, pw: str, loginsuccess=False) -> None:
    if loginsuccess:
        self.manager.current = "key_screen"
    else:
        self.manager.current = "incorrect_login_screen"
    return None


  def forgot_pw(self) -> None:
    app = App.get_running_app()
    sm = app.root.ids.sm
    sm.current = 'wip_screen'
    return None


  def close_app(self) -> None:
    exit()
    return None

class IncorrectLoginScreen(Screen):
    pass

class KeyScreen(Screen):

  class FileChooser(BoxLayout):


    def select(self, *args, root):
      # to get access to the label on the screen
      # which is one class level up
      # I pass the root class as a named argument
      try:
        self.selected_file = args[0][0]
        root.ids.label.text = self.selected_file
      except:
        self.selected_file = 'selected file'
        root.ids.label.text = self.selected_file
      return self.selected_file


    def load_file(self, root):
      # to get access to the label on the screen
      # which is one class level up
      # I pass the root class as a named argument
      with open(root.ids.label.text, 'r') as f:
        key_str = str(f.readline())
        f.close()
      #save key in scratch.txt
      with open('files/scratch.txt','w') as f2:
        f2.write(key_str)
        f2.close()
      root.manager.current = 'choice_screen'
      return None

class ChoiceScreen(Screen):
    def retrieve(self):
        pass

    def enter_new(self):
        app = App.get_running_app()
        sm = app.root.ids.sm
        sm.current = 'wip_screen'
        return None

    def edit_existing(self):
        app = App.get_running_app()
        sm = app.root.ids.sm
        sm.current = 'wip_screen'
        return None

class WorkInProgressScreen(Screen):
    @staticmethod
    def close_app():
        with open('files/scratch.txt', 'w') as f:
            f.write("")
            f.close()
        exit()

class OutputScreen(Screen):
    @staticmethod
    def close_app():
        with open('files/scratch.txt', 'w') as f:
            f.write("")
            f.close()
        exit()

class ScreenSelectButton(Button):
    # not used
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
        app, app_user_id = selection.split("-")
        app = app[5:].strip()
        app_user_id = app_user_id[7:].strip()
        # get the password
        # the user-variable holds the user of this app id of whom we want to retrieve the pw
        # the button name holds the app name and app iser id, not the vault app user id
        # we need to retrieve that
        user = get_vault_uid_from_record(app_user_id, app)
        pw = get_pw_from_record(user, app)
        #pw = 'test pw for now which is really long to see whether wrapping works'
        sm.get_screen('output_screen').ids.output_label_userid.text = app_user_id
        sm.get_screen('output_screen').ids.output_label_app.text = app
        sm.get_screen('output_screen').ids.output_label_pw.text = pw
        sm.current = 'output_screen'
        return None


class SwitchCreateScreensApp(App):
    def build(self):
        self.title = 'Password Vault'
        return Builder.load_file('gui.kv')



if __name__ == "__main__":
    SwitchCreateScreensApp().run()


