from fastapi import FastAPI

# from pydantic import BaseModel

import users, posts, auth, votes

# from database import get_db


app = FastAPI()


@app.get("/")
def home():
    # print("Welcome Home!")
    return {"msg ": "Welcome Home!"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)