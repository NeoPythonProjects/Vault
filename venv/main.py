from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from os.path import sep, expanduser, isdir, dirname
from kivy_garden.filebrowser import FileBrowser
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
import sys

from encryption import get_encryption_key, encrypt, decrypt
from decorators import logged_in
from login import encrypt_password


Builder.load_file('gui.kv')


class LoginScreen(Screen):

  @logged_in
  def log_in(self, user: str, pw: str) -> None:
    print("login success")
    #TODO: continue main code
    #Open main screen
    self.manager.current = "key_screen"
    return None


  def forgot_pw(self) -> None:
    print('forgot password')
    return None


  def close_app(self) -> None:
    sys.exit()
    return None


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
      print(self.selected_file)
      return self.selected_file

    def load_file(self, root):
      # to get access to the label on the screen
      # which is one class level up
      # I pass the root class as a named argument
      with open(root.ids.label.text) as f:
        key_str = f.readline()
      root.manager.current = 'login_screen'
      return key_str


class RootWidget(ScreenManager):
  pass


class MainApp(App):
  def build(self):
    return RootWidget()
  


@logged_in
def main(user: str, pw: str) -> None:
  print("login success")
  return None


if __name__ == "__main__":
  pass
  MainApp().run()
  # msg_utf = "testing 1 2 3 in the place to be"
  # key = get_encryption_key()
  # msg_enc_b = encrypt(msg_utf, key)
  # print(msg_enc_b)
  # msg = decrypt(msg_enc_b, key)
  # print(msg)
  # main(user='NeoPythonProjects', pw=encrypt_password(''))
  