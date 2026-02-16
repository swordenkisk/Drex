"""
gateway.main — FastAPI application for the Drex API Gateway.

Rules (per AGENTS.md):
- Routing and aggregation ONLY. No business logic here.
- Any route change must update the relevant gRPC/Protobuf contract.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Drex API Gateway",
    version="0.1.0",
    description="Routes HTTP requests to downstream gRPC microservices. No business logic.",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health", tags=["Infra"])
async def health() -> JSONResponse:
    """Liveness probe — returns 200 when the gateway process is alive."""
    return JSONResponse({"status": "ok"})


# ── Service routes ─────────────────────────────────────────────────────────
# Add APIRouter mounts below. Each router proxies to one downstream service.
#
# Example:
#   from gateway.routers import example_router
#   app.include_router(example_router.router, prefix="/example")
