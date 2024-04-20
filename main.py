from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class User(BaseModel):
    id: int 
    username: str
    email: str

users = list()
user_count = 0

@app.post("/create_user")
def create_user(username: str, email: str):
    global user_count
    new_user = User(id=user_count, username=username, email=email)
    users.append(new_user)
    user_count += 1 

    return new_user

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
        
    raise HTTPException(status_code=400, detail="Такого користувача нема")

@app.get("/users")
def get_all_users():
    return users