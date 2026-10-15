import json
from openai import OpenAI
from database import SessionLocal
import database_models

client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")   # key is ignored but required
MODEL = "llama3.1:8b"

def get_users(std: str | None = None) -> list[dict]:
    db = SessionLocal()
    try:
        q = db.query(database_models.User)
        if std:
            q = q.filter(database_models.User.std == std)
        return [{"id": u.id, "name": u.name, "age": u.age,
                 "std": u.std, "gender": u.gender} for u in q.all()]
    finally:
        db.close()

TOOLS = {"get_users": get_users}
TOOL_SPECS = [{
    "type": "function",
    "function": {
        "name": "get_users",
        "description": "List users from the database, optionally filtered by class, e.g. '10th'.",
        "parameters": {"type": "object", "properties": {"std": {"type": "string"}}},
    },
}]

def run_agent(question: str) -> str:
    messages = [{"role": "user", "content": question}]
    for _ in range(5):                       # loop cap, like max retries on a controller
        r = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SPECS)
        msg = r.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))
        if not msg.tool_calls:               # no tool requested: model is done
            return msg.content
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            print("tool call:", call.function.name, args)
            out = TOOLS[call.function.name](**args)
            messages.append({"role": "tool", "tool_call_id": call.id,
                             "content": json.dumps(out)})
    return "Stopped: too many tool calls"