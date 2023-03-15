from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from db import db
class User(BaseModel):
    username: str
    password: str

class Fungus(BaseModel):
    common_name: Optional[str] = None
    genus: str
    species: str
    description: Optional[str] = None
    habitat: Optional[str] = None
    edibility: Optional[str] = None

app = FastAPI()

@app.get("/")
def home():
  return {"Data" : "Go to the '/docs' endpoint to view all endpoints."}

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    user_id = db.create_user(user.username, user.password)
    return {"id": user_id}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user_data = db.get_user(user_id)
    if user_data is None or isinstance(user_data, int):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = {
        "id": user_data[0][0],
        "username": user_data[0][1],
        "password": user_data[0][2]
    }
    return user

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    success = await get_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.edit_user(user_id, user.username, user.password)
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete_user(user_id)
    return {"message": "User deleted successfully"}

@app.post("/fungi", status_code=status.HTTP_201_CREATED)
async def create_fungus(fungus: Fungus):
    fungus_id = db.create_fungus(fungus.common_name, fungus.genus, fungus.species, fungus.description, fungus.habitat, fungus.edibility)
    return {"fungus_id": fungus_id}

@app.get("/fungi/{fungus_id}")
async def get_fungus(fungus_id: int):
    fungus_data = db.get_fungus(fungus_id)
    if fungus_data is None or isinstance(fungus_data, int):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fungus not found")
    fungus = {
      "id": fungus_data[0][0],
      "common_name": fungus_data[0][1],
      "genus": fungus_data[0][2],
      "species": fungus_data[0][3],
      "description": fungus_data[0][4],
      "habitat": fungus_data[0][5],
      "edibility": fungus_data[0][6],
    }
    return fungus

@app.put("/fungi/{fungus_id}")
async def update_fungus(fungus_id: int, fungus: Fungus):
    success = db.edit_fungus(fungus_id, fungus.common_name, fungus.genus, fungus.species, fungus.description, fungus.habitat, fungus.edibility)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fungus not found")
    return {"message": "Fungus updated successfully"}

@app.delete("/fungi/{fungus_id}")
async def delete_fungus(fungus_id: int):
    success = db.get_fungus(fungus_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fungus not found")
    db.delete_fungus(fungus_id)
    return {"message": "Fungus deleted successfully"}

@app.get("/users/{user_id}/fungi")
async def get_user_fungi(user_id: int):
    fungi = db.get_user_fungi(user_id)
    return fungi

@app.post("/users/{user_id}/fungi/{fungus_id}")
async def add_user_fungus(user_id: int, fungus_id: int):
  success = db.add_user_fungus(user_id, fungus_id)
  if not success:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or fungus not found")
  return {"message": "Fungus added to user's collection successfully"}

@app.delete("/users/{user_id}/fungi/{fungus_id}")
async def remove_user_fungus(user_id: int, fungus_id: int):
  success = db.remove_user_fungus(user_id, fungus_id)
  if not success:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or fungus not found")
  return {"message": "Fungus removed from user's collection successfully"}