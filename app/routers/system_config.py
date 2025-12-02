from fastapi import APIRouter, HTTPException, status
from typing import List
from app import schemas
from app.services.system_config_service import SystemConfigService

router = APIRouter(prefix="/system-config", tags=["System Config"])

@router.get("/", response_model=List[schemas.SystemConfig])
def get_all_system_configs():
    return SystemConfigService.get_all_system_configs()

@router.get("/{config_key}", response_model=schemas.SystemConfig)
def get_system_config(config_key: str):
    config = SystemConfigService.get_system_config_by_key(config_key)
    if not config:
        raise HTTPException(status_code=404, detail="System config not found")
    return config

@router.post("/", response_model=schemas.SystemConfig, status_code=status.HTTP_201_CREATED)
def create_system_config(config: schemas.SystemConfigCreate):
    return SystemConfigService.create_system_config(config)

@router.put("/{config_key}", response_model=schemas.SystemConfig)
def update_system_config(config_key: str, config: schemas.SystemConfigUpdate):
    updated_config = SystemConfigService.update_system_config(config_key, config)
    if not updated_config:
        raise HTTPException(status_code=404, detail="System config not found")
    return updated_config

@router.delete("/{config_key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_system_config(config_key: str):
    SystemConfigService.delete_system_config(config_key)
    return None
