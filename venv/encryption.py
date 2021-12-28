from cryptography.fernet import Fernet


def get_encryption_key() -> bytes:
  # in GUI ask user to select text file to upload
  # for now, we use the scratch file
  src_file = 'files/scratch.txt'
  with open(src_file,'r') as f:
    key = f.readline().encode()
    f.close()
    return key


def encrypt(msg_utf: str, key: str):
  # Instance the Fernet class with the key
  fernet = Fernet(key)
  # then use the Fernet class instance
  # to encrypt the byte version of the string
  msg_enc_b = fernet.encrypt(msg_utf.encode())
  return msg_enc_b


def decrypt(msg_enc_b, key):
  # decrypt the encrypted string with the
  # Fernet instance of the key,
  # that was used for encrypting the string
  # encoded byte string is returned by decrypt method,
  # so decode it to string with decode methods
  fernet = Fernet(key)
  msg_dec_utf = fernet.decrypt(msg_enc_b).decode()
  return msg_dec_utf


if __name__ == "__main__":
  msg_utf = "testing 1 2 3 in the place to be"
  key = get_encryption_key()
  print(type(key))
  msg_enc_b = encrypt(msg_utf, key)
  print(msg_enc_b)
  msg = decrypt(msg_enc_b, key)
  print(msg)

  