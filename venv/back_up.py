# .py file containing one off bits of code
# left just in case I need them again
# but no if __name__ == "__main__" statement
# so that code can't be executed unintentionally

#from cryptography.fernet import Fernet
# deliberatly saved here without import statements
# this code is NOT TO BE RERUN once encryption
# has started, as it will replace the key needed for decryption
# i've alos changed the filename so it won't overwrite the
# original key in case someone runs this anyway

def create_encryption_key() -> None:
  # using symmetric encryption
  # generate a key for encryption and decryption
  # store this key safely
  #print(Fernet.generate_key().decode())
  #print(Fernet.generate_key())
  key = Fernet.generate_key().decode()
  with open('files/scratch.txt','w') as f:
    f.write(key) 
    f.close()
  # don't recreate every time
  return None


def convert_pw(user_pw_str="PASSWORD") -> hex:
  mdpass = md5(user_pw_str.encode())
  with open('tmppw.txt','w') as f:
    f.write(mdpass.hexdigest())
  return None 






