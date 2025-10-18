from supabase import create_client, Client
import os

# Class to Add the Supabase Client
class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_API_KEY")
        self.client: Client = create_client(self.url, self.key)

    # Insert Schedule
    def insert_schedule(self, tid, start, deadline, is_recurring, status, next_occurrence):
        db_data = {
            "tid": tid,
            "deadline": deadline,
            "status": status,
            "is_recurring": is_recurring,
            "next_occurrence": next_occurrence
        }
        if start is not None:
            db_data["start"] = start
        if next_occurrence is not None:
            db_data["next_occurrence"] = next_occurrence
            
        response = self.client.table("SCHEDULE").insert(db_data).execute()
        data = response.data
        return data[0] if data else None
    
    # Get Schedule by Task ID
    def fetch_schedule_by_tid(self, tid):
        response = self.client.table("SCHEDULE").select("*").eq("tid", tid).execute()
        data = response.data
        return data if data else None
    
    # Get Schedule by Schedule ID
    def fetch_schedule_by_sid(self, sid):
        response = self.client.table("SCHEDULE").select("*").eq("sid", sid).execute()
        data = response.data
        return data[0] if data else None

    # Delete Schedule
    def delete_schedule(self, sid):
        response = self.client.table("SCHEDULE").delete().eq("sid", sid).execute()
        data = response.data
        return data[0] if data else None

    # Update Schedule
    def update_schedule(self, sid, updated_data):
        if "is_recurring" in updated_data and updated_data["is_recurring"] is True:
            if "next_occurrence" not in updated_data:
                raise ValueError("next_occurrence is required when is_recurring is True")
        response = self.client.table("SCHEDULE").update(updated_data).eq("sid", sid).execute()
        data = response.data
        return data[0] if data else None