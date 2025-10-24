from supabase import create_client, Client
import os

# Class to Add the Supabase Client
class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_API_KEY")
        self.client: Client = create_client(self.url, self.key)

    # Insert Schedule
    def insert_schedule(self, tid, start, deadline, is_recurring, status, next_occurrence, frequency=None):
        # Validation for recurring schedules
        if is_recurring is True:
            if next_occurrence is None:
                raise ValueError("next_occurrence is required when is_recurring is True")
            if frequency is None:
                raise ValueError("frequency is required when is_recurring is True")
        
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
        if frequency is not None:
            db_data["frequency"] = frequency
            
        response = self.client.table("SCHEDULE").insert(db_data).execute()
        data = response.data
        return data[0] if data else None
    
    # Get Schedule by Task ID
    def fetch_schedule_by_tid(self, tid, latest=False):
        if latest:
            response = self.client.table("SCHEDULE").select("*").eq("tid", tid).order("created_at", desc=True).limit(1).execute()
            return response.data[0] if response.data else None
        response = self.client.table("SCHEDULE").select("*").eq("tid", tid).execute()
        return response.data if response.data else None
    
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
        if "is_recurring" in updated_data and updated_data["is_recurring"] is True and "next_occurrence" not in updated_data:
            raise ValueError("next_occurrence is required when is_recurring is True")

        response = self.client.table("SCHEDULE").update(updated_data).eq("sid", sid).execute()
        data = response.data
        return data[0] if data else None

    # Get all recurring tasks that need to be scheduled
    def fetch_recurring_tasks(self):
        response = self.client.table("SCHEDULE").select("*").eq("is_recurring", True).not_.is_("next_occurrence", "null").execute()
        return response.data if response.data else []