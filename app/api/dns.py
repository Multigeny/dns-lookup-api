import asyncio

from fastapi import APIRouter, HTTPException
from ipaddress import ip_address


from app.services.dns_resolver import lookup_records, reverse_lookup

router = APIRouter(prefix="/api/dns", tags=["DNS"])

@router.get("/lookup/{domain}")
async def lookup_dns(domain: str):
    
    ipv4, ipv6 = await asyncio.gather(
        lookup_records(domain, "A"),
        lookup_records(domain, "AAAA")
    )
    return {
        "domain": domain,
        "A": ipv4["records"],
        "AAAA": ipv6["records"],
        "success": ipv4["success"] or ipv6["success"]
    }

@router.get("/reverse/{ip}")
async def reverse_dns(ip: str):

    try:
        ip_address(ip)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid IP address"
        )

    return await reverse_lookup(ip)

@router.get("/mx/{domain}")
async def mx_lookup(domain: str):
    return await lookup_records(domain, "MX")


@router.get("/ns/{domain}")
async def ns_lookup(domain: str):
    return await lookup_records(domain, "NS")


@router.get("/txt/{domain}")
async def txt_lookup(domain: str):
    return await lookup_records(domain, "TXT")


@router.get("/all/{domain}")
async def all_lookup(domain: str):

    record_types = ["A", "AAAA", "MX", "NS", "TXT"]

    results = await asyncio.gather(
        *[
            lookup_records(domain, record_type)
            for record_type in record_types
        ]
    )

    records = {}

    for result in results:
        record_type = result["record_type"]

        records[record_type] = {
            "records": result["records"],
            "success": result["success"],
            "error": result.get("error")
        }

    return {
        "domain": domain,
        "records": results
    }
