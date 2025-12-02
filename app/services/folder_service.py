from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class FolderService:
    @staticmethod
    def get_all_folders() -> List[schemas.Folder]:
        response = supabase.table("folders").select("*").execute()
        return response.data

    @staticmethod
    def get_folder_by_id(folder_id: str) -> Optional[schemas.Folder]:
        response = supabase.table("folders").select("*").eq("folder_id", folder_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_folder(folder: schemas.FolderCreate) -> schemas.Folder:
        data = folder.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("folders").insert(data).execute()
        return response.data[0]

    @staticmethod
    def update_folder(folder_id: str, folder: schemas.FolderUpdate) -> Optional[schemas.Folder]:
        data = folder.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("folders").update(data).eq("folder_id", folder_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_folder(folder_id: str) -> None:
        supabase.table("folders").delete().eq("folder_id", folder_id).execute()
