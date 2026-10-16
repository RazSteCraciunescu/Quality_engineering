# Optional tools

`mcp_quality_server.py` exposes three read-only local tools: list events, inspect data-quality counters and suggest test scenarios. It is intentionally optional and does not modify registrations or connect to external systems.

```bash
pip install -e ".[mcp]"
python tools/mcp_quality_server.py
```
