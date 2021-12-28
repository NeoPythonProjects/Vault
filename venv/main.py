from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

from encryption import get_encryption_key, encrypt, decrypt
from decorators import logged_in
from login import encrypt_password

Builder.load_file('gui.kv')

class LoginScreen(Screen):
  pass

class RootWidget(ScreenManager):
  pass

class MainApp(App):
  def builder(self):
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
  #main(user='NeoPythonProjects', pw=encrypt_password(''))
  