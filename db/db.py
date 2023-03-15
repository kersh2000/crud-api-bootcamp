import sqlite3

def execute(sql, params=()):

  conn = sqlite3.connect('database.db')

  cursor = conn.cursor()

  try:
    cursor.execute(sql, params)
  except(Exception):
    print(f"SQL Error:\n SQL = {sql}\n Params = {params}")

  rows = cursor.fetchall()

  conn.commit()
  conn.close()

  if rows != []:
      return rows
  return cursor.lastrowid


def initialise():
    execute('''CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    execute('''CREATE TABLE IF NOT EXISTS fungi
    (id INTEGER PRIMARY KEY, common_name TEXT, genus TEXT, species TEXT, description TEXT, habitat TEXT, edibility TEXT)''')
    execute('''CREATE TABLE IF NOT EXISTS user_fungus
    (user_id INTEGER, fungus_id INTEGER, PRIMARY KEY(user_id, fungus_id), FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(fungus_id) REFERENCES fungi(id))''')

def reset():
  execute('''DROP TABLE IF EXISTS users''')
  execute('''DROP TABLE IF EXISTS fungi''')
  execute('''DROP TABLE IF EXISTS user_fungus''')
  initialise()

def create_user(username, password):
    id = execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
    return id

def get_user(user_id):
    user = execute('''SELECT * FROM users WHERE id=?''', (user_id,))
    return user

def edit_user(user_id, username=None, password=None):
    if username:
        execute('''UPDATE users SET username=? WHERE id=?''', (username, user_id))
    if password:
        execute('''UPDATE users SET password=? WHERE id=?''', (password, user_id))

def delete_user(user_id):
    execute('''DELETE FROM user_fungi WHERE user_id=?''', (user_id,))
    execute('''DELETE FROM users WHERE id=?''', (user_id,))

def create_fungus(common_name, genus, species, description, habitat, edibility):
    execute('''INSERT INTO fungi (common_name, genus, species, description, habitat, edibility) VALUES (?, ?, ?, ?, ?, ?)''', (common_name, genus, species, description, habitat, edibility))

def get_fungus(fungus_id):
    fungus = execute('''SELECT * FROM fungi WHERE id=?''', (fungus_id,))
    return fungus

def get_user_fungi(user_id):
    rows = execute('''SELECT fungi.* FROM fungi 
    JOIN user_fungus ON fungi.id = user_fungus.fungus_id
    WHERE user_fungus.user_id = ?''', (user_id,))
    return rows

def edit_fungus(fungus_id, **kwargs):
    set_clause = ", ".join([f"{k} = ?" for k in kwargs])
    values = list(kwargs.values()) + [fungus_id]
    execute(f"UPDATE fungi SET {set_clause} WHERE id = ?", tuple(values))

def delete_fungus(fungus_id):
    execute('''DELETE FROM user_fungi WHERE fungus_id=?''', (fungus_id,))
    execute('''DELETE FROM fungi WHERE id=?''', (fungus_id,))

def add_user_fungus(user_id, fungus_id):
    execute('''INSERT INTO user_fungus (user_id, fungus_id) VALUES (?, ?)''', (user_id, fungus_id))
