"""Optional read-only MCP server for local quality-assurance workflows.

Install the optional extra first: pip install -e .[mcp]
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from services.api.civicshift.database import Store
from services.api.civicshift.quality_assistant import generate_rule_based
from services.api.civicshift.settings import Settings

mcp = FastMCP("civicshift-quality")
settings = Settings.from_env()
store = Store(settings.database_path)


@mcp.tool()
def list_public_events() -> list[dict[str, object]]:
    """List fictional published events and current capacity state."""
    return store.list_events()


@mcp.tool()
def quality_snapshot() -> dict[str, object]:
    """Return critical local data-quality counters without modifying data."""
    return store.quality_snapshot()


@mcp.tool()
def suggest_test_scenarios(requirement: str, risk: str = "medium") -> dict[str, object]:
    """Generate deterministic test-design suggestions for an untrusted requirement string."""
    if risk not in {"low", "medium", "high"}:
        raise ValueError("risk must be low, medium or high")
    return generate_rule_based(requirement, risk)


if __name__ == "__main__":
    mcp.run()
