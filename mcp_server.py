from mcp.server.fastmcp import FastMCP
from database import SessionLocal
import database_models

mcp = FastMCP("users-tools", port=9000)

def _row(u) -> dict:
    return {"id": u.id, "name": u.name, "age": u.age, "std": u.std, "gender": u.gender, "email": u.email}

@mcp.tool()
def get_users(std: str | None = None) -> list[dict]:
    """List users from the database, optionally filtered by class, e.g. '10th'."""
    db = SessionLocal()
    try:
        q = db.query(database_models.User)
        if std:
            q = q.filter(database_models.User.std == std)
        return [_row(u) for u in q.all()]
    finally:
        db.close()

@mcp.tool()
def get_user_by_id(user_id: int) -> dict:
    """Get a single user by id. Returns an error message if not found."""
    db = SessionLocal()
    try:
        u = db.query(database_models.User).filter(database_models.User.id == user_id).first()
        return _row(u) if u else {"error": f"No user with id {user_id}"}
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run(transport="streamable-http")   # serves at http://localhost:9000/mcp