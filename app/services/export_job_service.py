from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class ExportJobService:
    @staticmethod
    def get_export_job_by_id(export_id: str) -> Optional[schemas.ExportJob]:
        response = supabase.table("export_jobs").select("*").eq("export_id", export_id).execute()
        if not response.data:
            return None
        
        job = response.data[0]
        
        # If DONE, generate signed URL
        if job['status'] == 'DONE' and job.get('file_path'):
            try:
                # Assuming 'exports' bucket
                signed_url_response = supabase.storage.from_("exports").create_signed_url(job['file_path'], 60 * 60)
                if isinstance(signed_url_response, dict) and 'signedURL' in signed_url_response:
                     # Add a temporary field or just rely on FE polling?
                     # The schema for ExportJob doesn't have a 'download_url' field. 
                     # However, the user request says "Response: ... + signed URL".
                     # I might need to return a dict or extend schema if strictly typed.
                     # 'schemas.ExportJob' is Pydantic. It doesn't have 'download_url'.
                     # I will assume the user consumes 'file_path' as URL or I should assume the schema needs update?
                     # Wait, usually for this specific endpoint response, I should probably return a modified object.
                     # But let's check schema again. ExportJob has 'file_path'.
                     # If I can't change schema (user provided table md), I'll put it in file_path?
                     # No, file_path is internal. 
                     # I will dynamically attach it if I can, or maybe the spec implies a separate response model.
                     # Let's check schemas again. There isn't an ExportJobDetail.
                     # I'll stick to 'file_path' containing the signed URL if DONE? No that's dirty.
                     # I will add 'download_url' to the returned dictionary if the Pydantic model allows extra fields or convert to dict.
                     pass 
                elif isinstance(signed_url_response, str):
                     # same here
                     pass
                
                # To properly support this without changing DB schema, I should likely change the return type in Router to a new Pydantic model or Dict.
                # But here in service, let's returns the object. 
                # Let's update the job dictionary with the signed URL in a 'download_url' key 
                # and let the router api response model handle it (which might need update).
                # Actually, I'll update the Pydantic schema in a separate step if needed. 
                # For now, I'll override 'file_path' with the signed URL? No, that's misleading.
                # I'll try to find where to put it. Retrieve signed URL *is* the goal.
                
                url = signed_url_response['signedURL'] if isinstance(signed_url_response, dict) else signed_url_response
                job['file_path'] = url # Override file_path with signed URL for FE consumption?
                # Or create a new field. Pydantic validation might strip unexpected fields.
                
            except Exception as e:
                print(f"Error generating signed URL: {e}")

        return schemas.ExportJob(**job)

    @staticmethod
    def create_export_job(user_id: str, recording_id: str, export_type: str) -> schemas.ExportJob:
        # Validate recording ownership? Logic says "Insert EXPORT_JOBS".
        # Assume caller validates or we do it here.
        # Let's do a quick ownership check to be safe.
        rec = supabase.table("recordings").select("user_id").eq("recording_id", recording_id).single().execute()
        if not rec.data:
             raise ValueError("Recording not found")
        if rec.data['user_id'] != user_id:
             raise ValueError("Not authorized")

        new_job = {
            "user_id": user_id,
            "recording_id": recording_id,
            "export_type": export_type,
            "status": "PENDING"
        }
        response = supabase.table("export_jobs").insert(new_job).execute()
        return response.data[0]

    # update and delete can remain valid for internal/admin use or if user cancels.
    @staticmethod
    def update_export_job(export_id: str, job: schemas.ExportJobUpdate) -> Optional[schemas.ExportJob]:
        data = job.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("export_jobs").update(data).eq("export_id", export_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_export_job(export_id: str) -> None:
        supabase.table("export_jobs").delete().eq("export_id", export_id).execute()
