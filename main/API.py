from fastapi import FastAPI
from .Routers import posts, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware


origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

app.include_router(posts.router)

app.include_router(vote.router)

app.include_router(auth.router)


@app.get("/")
def ask():
    return {"message": "Hello lil"}

