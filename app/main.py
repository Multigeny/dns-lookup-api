
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.api.dns import router as dns_router
from app.api.domains import router as domains_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await init_db()
#     yield


app = FastAPI(
    title="DNS Lookup API",
    description="REST API for DNS lookups and domain management",
    version="1.0.0"
)

app.include_router(dns_router)
app.include_router(domains_router)


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "healthy"
    }

