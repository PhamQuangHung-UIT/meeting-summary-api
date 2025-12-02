from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class SystemConfigService:
    @staticmethod
    def get_all_system_configs() -> List[schemas.SystemConfig]:
        response = supabase.table("system_config").select("*").execute()
        return response.data

    @staticmethod
    def get_system_config_by_key(config_key: str) -> Optional[schemas.SystemConfig]:
        response = supabase.table("system_config").select("*").eq("config_key", config_key).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_system_config(config: schemas.SystemConfigCreate) -> schemas.SystemConfig:
        data = config.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("system_config").insert(data).execute()
        return response.data[0]

    @staticmethod
    def update_system_config(config_key: str, config: schemas.SystemConfigUpdate) -> Optional[schemas.SystemConfig]:
        data = config.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("system_config").update(data).eq("config_key", config_key).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_system_config(config_key: str) -> None:
        supabase.table("system_config").delete().eq("config_key", config_key).execute()
