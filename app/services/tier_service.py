from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class TierService:
    @staticmethod
    def get_all_tiers() -> List[schemas.Tier]:
        response = supabase.table("tiers").select("*").execute()
        return response.data

    @staticmethod
    def get_tier_by_id(tier_id: int) -> Optional[schemas.Tier]:
        response = supabase.table("tiers").select("*").eq("tier_id", tier_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_tier(tier: schemas.TierCreate) -> schemas.Tier:
        data = tier.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("tiers").insert(data).execute()
        return response.data[0]

    @staticmethod
    def update_tier(tier_id: int, tier: schemas.TierUpdate) -> Optional[schemas.Tier]:
        data = tier.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("tiers").update(data).eq("tier_id", tier_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_tier(tier_id: int) -> None:
        supabase.table("tiers").delete().eq("tier_id", tier_id).execute()
