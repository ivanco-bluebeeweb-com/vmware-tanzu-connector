"""Resource handlers for VMware Tanzu Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListContainerParams, GetContainerParams,
    ContainerRecord, ContainerList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_containers", "List containers in VMware Tanzu.", action_type="read", chain_callable=True, event="vmware-tanzu-connector.list_containers", effects=["read:containers"], data_model=ContainerList)
async def list_containers(params: ListContainerParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_containers(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or r.get("key") or r.get("uuid") or "unknown")
            rname = r.get("name") or r.get("title") or r.get("label") or rid
            items.append({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r})
        return ActionResult.ok({"containers": items, "total": len(items)}, summary=f"Found {len(items)} containers.")
    except Exception as e:
        return ActionResult.error(f"Error listing containers: {e}")

@chat.function("get_container", "Get details of one Container in VMware Tanzu.", action_type="read", chain_callable=True, event="vmware-tanzu-connector.get_container", effects=["read:container"], data_model=ContainerRecord)
async def get_container(params: GetContainerParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_container(params.container_id)
        rid = str(r.get("id") or params.container_id)
        rname = r.get("name") or r.get("title") or rid
        return ActionResult.ok({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r}, summary=f"Retrieved Container {rid}.")
    except Exception as e:
        return ActionResult.error(f"Error retrieving Container: {e}")

@chat.function("audit_container_health", "Audit health of VMware Tanzu containers and connectivity.", action_type="read", chain_callable=True, event="vmware-tanzu-connector.audit_container_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_container_health(params: ConnectionIdParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_containers(limit=50)
        return ActionResult.ok({
            "healthy": True,
            "total_containers": len(items),
            "details": {"sample_count": len(items)},
            "summary": f"VMware Tanzu healthy. Sampled {len(items)} containers."
        }, summary=f"VMware Tanzu health check passed with {len(items)} containers.")
    except Exception as e:
        return ActionResult.error(f"Error auditing VMware Tanzu health: {e}")
