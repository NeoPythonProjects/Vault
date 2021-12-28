from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from os.path import sep, expanduser, isdir, dirname
from kivy_garden.filebrowser import FileBrowser
from kivy.utils import platform
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

  def show_file_browser(self):
    if platform == 'win':
        user_path = dirname(expanduser('~')) + sep + 'Documents'
    else:
        user_path = expanduser('~') + sep + 'Documents'
    browser = FileBrowser(select_string='Select',
                          favorites=[(user_path, 'Documents')])
    browser.bind(
                on_success=self._fbrowser_success,
                on_canceled=self._fbrowser_canceled)
    return browser

  def _fbrowser_canceled(self, instance):
      print ('cancelled, Close self.')

  def _fbrowser_success(self, instance):
      print (instance.selection)


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
  