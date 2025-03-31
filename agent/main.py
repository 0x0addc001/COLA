import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
# from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
# from contextlib import asynccontextmanager

from formulation_agent.graph import graph as formulation_graph

app = FastAPI()
sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="formulation_agent",
            description="Formulation Agent",
            graph=formulation_graph,
        ),
        # LangGraphAgent(
        #     name="translation_agent",
        #     description="Translation Agent",
        #     graph=translation_graph,
        # ),
        # LangGraphAgent(
        #     name="visualization_agent",
        #     description="Visualization Agent",
        #     graph=visualization_graph,
        # ),
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
