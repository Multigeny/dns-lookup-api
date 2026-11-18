
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.domain import Domain
from app.schemas.domain import (
    DomainCreate,
    DomainUpdate,
    DomainResponse
)


router = APIRouter(
    prefix="/api/domains",
    tags=["Domains"]
)


@router.post("", response_model=DomainResponse, status_code=status.HTTP_201_CREATED)
async def create_domain(
    data: DomainCreate,
    db: AsyncSession = Depends(get_db)
):

    domain = Domain(
        domain=data.domain,
        description=data.description
    )

    db.add(domain)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Domain already exists"
        )

    await db.refresh(domain)

    return domain



@router.get("", response_model=list[DomainResponse])
async def get_domains(db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(Domain))

    return result.scalars().all()



@router.get("/{domain_id}", response_model=DomainResponse)
async def get_domain(domain_id: int, db: AsyncSession = Depends(get_db)):

    domain = await db.get(Domain, domain_id)

    if domain is None:
        raise HTTPException(
            status_code=404,
            detail="Domain not found"
        )

    return domain



@router.put("/{domain_id}", response_model=DomainResponse)
async def update_domain(domain_id: int, data: DomainUpdate, db: AsyncSession = Depends(get_db)):
    
    domain = await db.get(Domain, domain_id)

    if domain is None:
        raise HTTPException(
            status_code=404,
            detail="Domain not found"
        )

    domain.domain = data.domain
    domain.description = data.description

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Domain already exists"
        )

    await db.refresh(domain)

    return domain



@router.delete("/{domain_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_domain(domain_id: int, db: AsyncSession = Depends(get_db)):

    return {
        "status": "Delete тоже добавлен"
    }
    # domain = await db.get(Domain, domain_id)

    # if domain is None:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="Domain not found"
    #     )

    # await db.delete(domain)
    # await db.commit()

    # return Response(status_code=status.HTTP_204_NO_CONTENT)
