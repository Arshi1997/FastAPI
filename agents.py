from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.models.ollama import Ollama          # replaces the Gemini/Claude import
from agno.tools.mcp import MCPTools

ops_agent = Agent(
    id="ops-agent",
    name="Ops Agent",
    model=Ollama(id="llama3.1:8b"),
    db=SqliteDb(db_file="agno.db"),
    tools=[MCPTools(transport="streamable-http", url="http://localhost:9000/mcp")],
    add_history_to_context=True,
    debug_mode=True,
)

docs_agent = Agent(
    id="docs-agent",
    name="Microsoft Docs Agent",
    model=Ollama(id="llama3.1:8b"),
    db=SqliteDb(db_file="agno.db"),
    tools=[MCPTools(transport="streamable-http", url="https://learn.microsoft.com/api/mcp")],
    instructions=["Answer Microsoft and Azure questions by searching the docs tools first, and list the page URLs you used."],
    add_history_to_context=True,
)