from supabase import create_client, Client
import os

# Class to Add the Supabase Client
class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_API_KEY")
        self.client: Client = create_client(self.url, self.key)
   
    # Insert Schedule
    def insert_schedule(self, tid, deadline, status):
        # if self.fetch_schedule(tid) is not None: #Assumption is that one task cannot have MULTIPLE DEADLINES
        #     raise Exception("Task with this ID already exists.")
        response = self.client.table("SCHEDULE").insert({
            "tid": tid,
            "deadline": deadline,
            "status": status
        }).execute()
        data = response.data
        return data[0] if data else None
    
    # Get Schedule
    def fetch_schedule(self, tid):
        response = self.client.table("SCHEDULE").select("*").eq("tid", tid).execute()
        data = response.data
        return data[0] if data else None
   
    # Delete Schedule
    def delete_schedule(self, tid):
        response = self.client.table("SCHEDULE").delete().eq("tid", tid).execute()
        data = response.data
        return data[0] if data else None
   
    # Update Schedule
    def update_schedule(self, tid, updated_data):
        response = self.client.table("SCHEDULE").update(updated_data).eq("tid", tid).execute()
        data = response.data
        return data[0] if data else None