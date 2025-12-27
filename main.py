from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from pydantic import BaseModel

import users, posts, auth, votes

# from database import get_db


app = FastAPI()


@app.get("/")
def home():
    # print("Welcome Home!")
    return {"msg ": "Welcome Home!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or 3000, etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)