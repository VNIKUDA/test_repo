from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import json

# Форма користувача
class User(BaseModel):
    username: str
    email: str

# Частина для роботи з базою данних
database = "users.db"
conn = None
cursor = None

# Відкриття та закриття бази даних
def open():
    global conn, cursor
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

# SQL запит
def do(query):
    cursor.execute(query)
    conn.commit()

# Створення всіх таблиць (в даному випадку тільки users)
def create_all():
    open()

    do('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            username VARCHAR, 
            email VARCHAR
       )''')

    close()

# Додавання користувача
def add_user(user: User):
    open()

    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", [user.username, user.email])
    conn.commit()

    close()

    return user

# Пошук користувача по id
def get_user(user_id: int):
    open()

    cursor.execute("SELECT * FROM users WHERE id == ?", (str(user_id), ))
    user = cursor.fetchall()[0]

    close()

    return user

# Всі користувачі
def users():
    open()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    close()

    return users

# Ініціалізація бази даних
create_all()


# FastAPI 
app = FastAPI()

# Створення користувача
@app.post("/create_user")
def create_user(username: str, email: str):
    new_user = User(username=username, email=email)

    return add_user(new_user)

# Користувач по id 
@app.get("/users/{user_id}")
def get_user(user_id: int):
    users_ = users()
    for user in users_:
        if user[0] == user_id:
            return user
        
    raise HTTPException(status_code=400, detail="Такого користувача нема")

# Всі користувачі
@app.get("/users")
def get_all_users():
    return users()