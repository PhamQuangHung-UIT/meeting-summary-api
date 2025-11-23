from fastapi import APIRouter, HTTPException, status
from typing import List
from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/tiers", tags=["Tiers"])

@router.get("/", response_model=List[schemas.Tier])
def get_all_tiers():
    response = supabase.table("tiers").select("*").execute()
    return response.data

@router.get("/{tier_id}", response_model=schemas.Tier)
def get_tier(tier_id: int):
    response = supabase.table("tiers").select("*").eq("tier_id", tier_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Tier not found")
    return response.data[0]

@router.post("/", response_model=schemas.Tier, status_code=status.HTTP_201_CREATED)
def create_tier(tier: schemas.TierCreate):
    response = supabase.table("tiers").insert(tier.model_dump(exclude_unset=True)).execute()
    return response.data[0]

@router.put("/{tier_id}", response_model=schemas.Tier)
def update_tier(tier_id: int, tier: schemas.TierUpdate):
    response = supabase.table("tiers").update(tier.model_dump(exclude_unset=True)).eq("tier_id", tier_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Tier not found")
    return response.data[0]

@router.delete("/{tier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tier(tier_id: int):
    supabase.table("tiers").delete().eq("tier_id", tier_id).execute()
    return None
