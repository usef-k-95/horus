"""horus_state — the Horus engagement-state backend.

One YAML file per record under `<engagement>/.horus/`, an append-only event log, a derived
SQLite index, integrity rules, approvals, gate checklists, views, an MCP server and the
`horus` command line. The published JSON Schema (`horus schema export`) is the contract that
the plugin, the meeting runtime and any future portal speak.
"""

__all__ = ["__version__", "SCHEMA_VERSION"]
__version__ = "0.1.0"
SCHEMA_VERSION = "0.2.0"
