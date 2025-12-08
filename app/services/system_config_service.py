from typing import List, Optional
from app.utils.database import supabase

import schemas

class SystemConfigService:
    @staticmethod
    def get_system_config_by_key(config_key: str) -> Optional[schemas.SystemConfig]:
        result = supabase.table("system_config").select("*").eq("config_key", config_key).execute()
        if result.data:
            return result.data[0]
        return None
    
    @staticmethod
    def get_system_configs_by_group(config_group: str) -> List[schemas.SystemConfig]:
        result = supabase.table("system_config").select("*").eq("config_group", config_group).execute()
        return result.data
    
    @staticmethod
    def create_system_config(config: schemas.SystemConfigCreate) -> schemas.SystemConfig:
        data = config.model_dump(mode='json', exclude_unset=True)
        result = supabase.table("system_config").insert(data).execute()
        return result.data[0]
    
    @staticmethod
    def update_system_config(config_key: str, config_update: schemas.SystemConfigUpdate) -> Optional[schemas.SystemConfig]:
        data = config_update.model_dump(mode='json', exclude_unset=True)
        result = supabase.table("system_config").update(data).eq("config_key", config_key).execute()
        if result.data:
            return result.data[0]
        return None
    
    @staticmethod
    def delete_system_config(config_key: str) -> bool:
        result = supabase.table("system_config").delete().eq("config_key", config_key).execute()
        return len(result.data) > 0