from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import bcrypt
from fastapi.staticfiles import StaticFiles
import os


app = FastAPI()


# Enable CORS (for development; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5500"] if you know the frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Connect to MongoDB (use `todolistdb`)
# Example MongoDB connection string:
client = MongoClient("mongodb://mongodb:27017")
db = client["todolistdb"]
users_collection = db["users"]

# Pydantic models
class User(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

# Signup endpoint
@app.post("/api/signup")
def signup(user: User):
    # Check if email already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    # Insert new user
    users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_password  # Store hashed password
    })

    return {"message": "Signup successful"}

# Login endpoint
@app.post("/api/login")
def login(user: Login):
    # print("Logging in user:")
    found = users_collection.find_one({"email": user.email})
    if not found:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not bcrypt.checkpw(user.password.encode('utf-8'), found['password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful"}


