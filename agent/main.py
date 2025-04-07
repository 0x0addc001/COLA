import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
# from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
# from contextlib import asynccontextmanager

from cola.graph import graph

app = FastAPI()
sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="cola",
            description="cola",
            graph=graph,
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")


# add new route for health check
@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}

def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=port,
        reload=True,
        reload_dirs=(
            ["."] +
            (["../../sdk-python/copilotkit"]
             if os.path.exists("../../sdk-python/copilotkit")
             else []
             )
        )
    )
