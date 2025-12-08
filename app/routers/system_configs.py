from fastapi import APIRouter, HTTPException, status
from typing import List
from app import schemas
from app.services.system_config_service import SystemConfigService

router = APIRouter(prefix="/config", tags=["System Config"])

@router.get("/{config_key}", response_model=schemas.SystemConfig)
def get_system_config(config_key: str):
    config = SystemConfigService.get_system_config_by_key(config_key)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config

@router.get("/configGroup={config_group}", response_model=List[schemas.SystemConfig])
def get_system_configs_by_group(config_group: str):
    configs = SystemConfigService.get_system_configs_by_group(config_group)
    if not configs:
        raise HTTPException(status_code=404, detail="No configs found for the specified group")
    return configs

@router.put("/{config_key}", response_model=schemas.SystemConfig)
def update_system_config(config_key: str, config: schemas.SystemConfigUpdate):
    updated_config = SystemConfigService.update_system_config(config_key, config)
    if not updated_config:
        raise HTTPException(status_code=404, detail="Config not found")
    return updated_config

@router.delete("/{config_key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_system_config(config_key: str):
    success = SystemConfigService.delete_system_config(config_key)
    if not success:
        raise HTTPException(status_code=404, detail="Config not found")
    return