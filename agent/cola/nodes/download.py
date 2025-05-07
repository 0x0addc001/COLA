"""
This module contains the implementation of the download_node function.
"""

import aiohttp
import html2text
from copilotkit.langgraph import copilotkit_emit_state
from langchain_core.runnables import RunnableConfig
import textwrap

from cola.state import AgentState

_REFERENCE_CACHE = {}

def get_reference(url: str):
    """
    Get a reference from the cache.
    """
    return _REFERENCE_CACHE.get(url, "")

#  Mimicking a Chrome browser’s User-Agent, the request could bypass basic anti-scraping measures
_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" # pylint: disable=line-too-long

async def _download_reference(url: str):
    """
    Download a reference from the internet asynchronously.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={"User-Agent": _USER_AGENT},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                response.raise_for_status()
                html_content = await response.text()
                markdown_content = html2text.html2text(html_content)

                # Truncate the markdown content if it exceeds 10000 characters
                markdown_content = textwrap.shorten(markdown_content, width=10000, placeholder="...")

                _REFERENCE_CACHE[url] = markdown_content
                return markdown_content
    except Exception as e: # pylint: disable=broad-except
        _REFERENCE_CACHE[url] = "ERROR"
        return f"下载错误: {e}"

async def download_node(state: AgentState, config: RunnableConfig):
    """
    Download references from the internet.
    """
    state["references"] = state.get("references", [])
    state["logs"] = state.get("logs", [])
    references_to_download = []

    logs_offset = len(state["logs"])

    # Find references that are not downloaded
    for reference in state["references"]:
        if not get_reference(reference["url"]):
            references_to_download.append(reference)
            state["logs"].append({
                "message": f"正在下载 {reference['url']}",
                "done": False
            })

    # Emit the state to let the UI update
    await copilotkit_emit_state(config, state)

    # Download the references
    for i, reference in enumerate(references_to_download):
        await _download_reference(reference["url"])
        state["logs"][logs_offset + i]["done"] = True

        # update UI
        await copilotkit_emit_state(config, state)

    return state
