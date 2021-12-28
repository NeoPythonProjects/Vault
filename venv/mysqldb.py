from decorators import execute_sql
from login import encrypt_password
from encryption import get_encryption_key, decrypt, encrypt


#retrieve records
#----------------
@execute_sql('runquery')
def get_pw_from_record_cursor(usr: str, app: str) -> str:
  return """
  SELECT app_user_id, app_hash 
  FROM applications
  WHERE (user_name = ? 
  AND application = ?)
  """

def get_pw_from_record(usr: str, app: str) -> str:
  # link to password box in GUI
  pw_b = get_pw_from_record_cursor(usr, app)[0][1]
  pw_str = decrypt(pw_b, get_encryption_key())
  return pw_str


def get_app_user_id_from_record(usr: str, app: str) -> str:
  # link to app_user_ID box in GUI
  return get_pw_from_record_cursor(usr, app)[0][0]


# read tables
#------------
@execute_sql('read')
def read_table(*_, tb: str) -> str:
  return  f"""
  SELECT *
  FROM {tb}
  """

# check database fields
#----------------------
@execute_sql('read')
def show_field_names() -> str:
  sqlstr = f"""SELECT 
  m.name as table_name, 
  p.name as column_name
FROM 
  sqlite_master AS m
JOIN 
  pragma_table_info(m.name) AS p
ORDER BY 
  m.name, 
  p.cid"""
  return sqlstr

# create tables
# -------------
@execute_sql('write')
def create_table_users() -> str:
  sqlstr = """CREATE TABLE IF NOT EXISTS users (
    user_name VARCHAR(20),
    user_hash VARCHAR(255)
  )"""
  return sqlstr


@execute_sql('write')
def create_table_applications() -> str:
  sqlstr = """CREATE TABLE IF NOT EXISTS applications (
    user_name VARCHAR(20),
    application VARCHAR(100),
    app_user_id VARCHAR(100),
    app_hash VARCHAR(255)
  )"""
  return sqlstr


# insert_users
#-------------
@execute_sql('write')
def insert_users(user: str, pw_hex: hex) -> str:
  return """
  INSERT INTO users
  VALUES (?,?)
  """


def enter_users_in_db():
  usr = input("user: ")
  pw = input("password (can be read, for internal use only: ")
  pw_hex = encrypt_password(pw)
  insert_users(usr,pw_hex)


@execute_sql('write')
def insert_apps(user_name: str, application: str, app_user_id: str, app_hash: hex) -> str:
  return """
  INSERT INTO applications
  VALUES (?,?,?,?)
  """

def enter_applications_record() -> None:
  # via GUI in future
  # from dropdowns, so no need to check user exists
  key = get_encryption_key()
  usr = 'NeoPythonProjects'
  app = 'test_app'
  app_usr_id = 'Neo'
  app_hash = encrypt('1234', key)
  insert_apps(usr, app, app_usr_id, app_hash)
  return None



# delete all entries
#-------------------
@execute_sql('write')
def clean_table(*_, tb: str) -> str:
  return f"""
DELETE FROM {tb}
"""

if __name__ == "__main__":
  pass
  #clean_table(tb='applications')
  # enter_applications_record()
  #enter_users_in_db()
  #read_table(tb='applications')
  #create_table_applications() 
  #show_field_names()
  
  print(get_app_user_id_from_record('NeoPythonProjects','test_app'), get_pw_from_record('NeoPythonProjects','test_app'))