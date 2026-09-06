"""Extension declaration, capabilities, health check for VMware Tanzu Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "vmware-tanzu-connector",
    version="0.1.0",
    display_name="VMware Tanzu",
    icon="icon.svg",
    capabilities=["vmware_tanzu:manage"],
    description="Official Imperal connector for VMware Tanzu (C30. Email Marketing & Newsletter). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("vmware_tanzu_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} VMware Tanzu connection(s) configured." if count else "Not connected yet."
    }
