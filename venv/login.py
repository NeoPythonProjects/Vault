from hashlib import md5
import sys


# def checkPassword(stored_pw: hex):
#     for key in range(3):
#         #get the user's password as string
#         user_pw_str = input("Enter the password: ")
#         # create an md5 object
#         # takes bytes as input via str.encode()
#         mdpass = md5(user_pw_str.encode())
#         # output encrypted password as hex
#         # and compare to stored password in hex
#         if mdpass.hexdigest() == stored_pw:
#             #password correct
#             return True
#         else:
#             print('wrong password, try again')
#     print('you have failed')
#     return False
#

def get_stored_pwd(user: str) -> hex:
  # user is not used in the text file
  # but will be used when we hve the login table
  # read stored password in hex
  with open('files/tmppw.txt','r') as f:
      return f.read()


def encrypt_password(pw: str) -> hex:
  # convert pw to bytes using str.encode()
  return md5(pw.encode()).hexdigest()


def main():
  user=""
  user_pw_hex = get_stored_pwd(user)
  if checkPassword(user_pw_hex):
      print("You're in")
      #continue to do stuff
      
  else:
      sys.exit()



if __name__ == '__main__':
  pass
  main()
