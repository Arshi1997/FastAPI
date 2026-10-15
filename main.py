from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from users import user
import database_models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from dotenv import load_dotenv
load_dotenv()                      # reads ANTHROPIC_API_KEY from .env in the project root

from pydantic import BaseModel
from agent_loop import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

users = [
    user(id=1, name="Alice", age=25, std="10th", gender="Female", email="alice@example.com"),
    user(id=2, name="Bob", age=30, std="12th", gender="Male", email="bob@example.com"),
    user(id=3, name="Charlie", age=22, std="11th", gender="Male", email="charlie@example.com"),
    user(id=4, name="David", age=28, std="10th", gender="Male", email="david@example.com"),
    user(id=5, name="Eve", age=27, std="12th", gender="Female", email="eve@example.com"),
    user(id=6, name="Frank", age=24, std="11th", gender="Male", email="frank@example.com"),
    user(id=7, name="Grace", age=26, std="10th", gender="Female", email="grace@example.com"),
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()

    count = db.query(database_models.User).count()

    if count == 0:
        for user_obj in users:
            db.add(database_models.User(**user_obj.model_dump()))

        db.commit()

    db.close()

init_db()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Hello, welcome to the program!", "users": db.query(database_models.User).all()}

@app.get("/api/users")
def read_users(db: Session = Depends(get_db)):
    #db connection and query logic here
    users = db.query(database_models.User).all()
    db.close()
    return {"message": "Here are the users!", "users": users}

@app.get("/api/stats")
def read_stats(db: Session = Depends(get_db)):
    return {"message": "Here are the statistics!"}

@app.get("/api/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(database_models.User).all()
    db.close()
    return {"message": "Here are the users!", "users": users}

@app.get("/api/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(database_models.User).filter(database_models.User.id == user_id).first()
    db.close()
    if not user:
        return {"message": "User not found"}
    return {"message": f"Here is the user with ID: {user_id}", "user": user}

@app.post("/api/users")
def create_user(new_user: user, db: Session = Depends(get_db)):
    db.add(database_models.User(**new_user.model_dump()))
    db.commit()
    db.close()
    return {"message": "User created successfully", "user": new_user}

@app.put("/api/users/{user_id}")
def update_user(user_id: int, updated_user: user, db: Session = Depends(get_db)):
    user = db.query(database_models.User).filter(database_models.User.id == user_id).first()
    if not user:
        db.close()
        return {"message": "User not found"}
    for key, value in updated_user.model_dump().items():
        setattr(user, key, value)
    db.commit()
    db.close()
    return {"message": "User updated successfully", "user": user}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(database_models.User).filter(database_models.User.id == user_id).first()
    if not user:
        db.close()
        return {"message": "User not found"}
    db.delete(user)
    db.commit()
    db.close()
    return {"message": "User deleted successfully"}

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat/agent")       # Stage 2: hand-written loop
def chat_agent(req: ChatRequest):
    return {"reply": run_agent(req.message)}

# Stage 3+: AgentOS wraps your app. Must come after all routes, before __main__.
from agno.os import AgentOS
from agents import ops_agent, docs_agent          # changed - using 2 agents now

agent_os = AgentOS(
    agents=[ops_agent, docs_agent],               # changed - using 2 agents now
    base_app=app,
    on_route_conflict="preserve_base_app",
    tracing=True,
)
app = agent_os.get_app()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("PORT", 8000)))