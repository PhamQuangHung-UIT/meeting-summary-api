from fastapi import APIRouter, HTTPException, status
from typing import List
from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/system-config", tags=["System Config"])

@router.get("/", response_model=List[schemas.SystemConfig])
def get_all_system_configs():
    response = supabase.table("system_config").select("*").execute()
    return response.data

@router.get("/{config_key}", response_model=schemas.SystemConfig)
def get_system_config(config_key: str):
    response = supabase.table("system_config").select("*").eq("config_key", config_key).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="System config not found")
    return response.data[0]

@router.post("/", response_model=schemas.SystemConfig, status_code=status.HTTP_201_CREATED)
def create_system_config(config: schemas.SystemConfigCreate):
    response = supabase.table("system_config").insert(config.model_dump(exclude_unset=True)).execute()
    return response.data[0]

@router.put("/{config_key}", response_model=schemas.SystemConfig)
def update_system_config(config_key: str, config: schemas.SystemConfigUpdate):
    response = supabase.table("system_config").update(config.model_dump(exclude_unset=True)).eq("config_key", config_key).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="System config not found")
    return response.data[0]

@router.delete("/{config_key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_system_config(config_key: str):
    supabase.table("system_config").delete().eq("config_key", config_key).execute()
    return None
