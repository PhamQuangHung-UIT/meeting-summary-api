from fastapi import APIRouter, HTTPException, status
from typing import List
from app import schemas
from app.services.tier_service import TierService

router = APIRouter(prefix="/tiers", tags=["Tiers"])

@router.get("/", response_model=List[schemas.Tier])
def get_all_tiers():
    return TierService.get_all_tiers()

@router.get("/{tier_id}", response_model=schemas.Tier)
def get_tier(tier_id: int):
    tier = TierService.get_tier_by_id(tier_id)
    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    return tier

@router.post("/", response_model=schemas.Tier, status_code=status.HTTP_201_CREATED)
def create_tier(tier: schemas.TierCreate):
    return TierService.create_tier(tier)

@router.put("/{tier_id}", response_model=schemas.Tier)
def update_tier(tier_id: int, tier: schemas.TierUpdate):
    updated_tier = TierService.update_tier(tier_id, tier)
    if not updated_tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    return updated_tier

@router.delete("/{tier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tier(tier_id: int):
    TierService.delete_tier(tier_id)
    return None
