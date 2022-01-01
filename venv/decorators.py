import functools
import sqlite3
from login import encrypt_password
from sys import exit


def logged_in(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    for k,v in kwargs.items():
      if k == "user": user = v
      if k == "pw": pw = v
    #check user credentials
    if user_exists(user) and get_stored_pw(user) == encrypt_password(pw):
      #execute func
      fn = func(*args,user=user, pw=pw, loginsuccess = True)
      #return func
      return fn
    else:
      print("incorrect login details")
      fn = func(*args, user=user, pw=pw, loginsuccess=False)
      return False
  return wrapper  


def execute_sql(action):
  """ decorator takes 1 'action' argument.
  It connects to db, creates cursor, executes cursor, commits to db if required and closes db connection.

  decorator combines the show_records and insert_record decorators

  argument: action can be 'read' or 'write'
  'read' lists the query results line by line to shell
  'write' writes to database
  'runquery' returns the query result
  
  func: returns a sql string where args are passed as ? as part of execute and kwargs are passed as f-string variables (cur.execute doesn't accept named arguments)
  """ 
  # decorator takes action as argument
  # needs an extra level that accepts the argument and return a decorator
  #action can be (i) write or (ii) read or (iii) runquery
  def decorator(func):
    # keep introspection of inner functions intact
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      #connect to database
      db = 'files/db.db'
      conn = sqlite3.connect(db)
      cur = conn.cursor()
      #execute func
      sqlstr= func(*args, **kwargs)
      result = cur.execute(sqlstr, args)
      if action == "write":
        conn.commit()
      elif action == "read":
        for el in result:
          print(el) 
      elif action == 'runquery':
        result = result.fetchall()
        # in this case return the results, not the sqlstr
        return result
      conn.close()
      #return function object
      return sqlstr
    return wrapper
  return decorator


# login subqueries
#------------------
@execute_sql('runquery')
def get_stored_pw_cursor(user: str) -> str:
  return """
  SELECT user_hash
  FROM users
  WHERE user_name = ?
  """

def get_stored_pw(user: str) -> str:
  return get_stored_pw_cursor(user)[0][0]


@execute_sql('runquery')
def user_exists_cursor(user: str) -> str:
  sqlstr = """
  SELECT user_name 
  FROM users
  WHERE user_name = ?
  """
  return sqlstr
  

def user_exists(user: str) -> bool:  
  # Pythonic: an empty list is False
  if not user_exists_cursor(user):
    return False
    exit()
  return True


if __name__ == "__main__":
  #print(get_stored_pw('NeoPythonProjects'))
  #print(user_exists('NeoPythonProjects'))
  pass