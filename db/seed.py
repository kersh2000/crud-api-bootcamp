from db import db

def seed():
  users = [
    {"username": "alice", "password": "password1"},
    {"username": "bob", "password": "password2"},
    {"username": "charlie", "password": "password3"}
  ]

  fungi = [
    {"common_name": "fly agaric", "genus": "Amanita", "species": "muscaria", "description": "A bright red and white mushroom with a distinctive cap and stem.", "habitat": "Found in woodland areas in Europe and North America.", "edibility": "Toxic, hallucinogenic."},
    {"common_name": "chanterelle", "genus": "Cantharellus", "species": "cibarius", "description": "A yellow to orange mushroom with a wavy cap and stem.", "habitat": "Found in forests and woodland areas in Europe and North America.", "edibility": "Edible, highly prized by chefs."},
    {"common_name": "king bolete", "genus": "Boletus", "species": "edulis", "description": "A large, meaty mushroom with a brown cap and stem.", "habitat": "Found in forests and woodland areas in Europe and North America.", "edibility": "Edible, highly prized by mushroom hunters."},
  ]

  db.reset()

  for user in users:
    db.create_user(user["username"], user["password"])

  for fungus in fungi:
    db.create_fungus(fungus["common_name"], fungus["genus"], fungus["species"], fungus["description"], fungus["habitat"], fungus["edibility"])

  user_ids = [1, 1, 2, 3]
  fungus_ids = [1, 3, 2, 3]

  for i in range(3):
    db.add_user_fungus(user_ids[i], fungus_ids[i])

  print("Seed data has been added to the database.")
