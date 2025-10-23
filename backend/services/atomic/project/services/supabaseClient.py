from supabase import create_client, Client
import os

# Class to Add the Supabase Client
class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_API_KEY")
        self.client: Client = create_client(self.url, self.key)
    
    # Insert Project
    def insert_project(self, uid, name, desc):
        response = self.client.table("PROJECT").insert({
            "uid": uid,
            "name": name,
            "desc": desc
        }).execute()
        data = response.data
        return data[0] if data else None
    
    # Get Project by Project ID
    def fetch_project_by_pid(self, pid):
        response = self.client.table("PROJECT").select("*").eq("id", pid).execute()
        data = response.data
        return data[0] if data else None
    
    # Get Project by User ID
    def fetch_project_by_uid(self, uid):
        response = self.client.table("PROJECT").select("*").eq("uid", uid).execute()
        data = response.data
        return data if data else None
    
    # Delete Project
    def delete_project(self, pid):
        response = self.client.table("PROJECT").delete().eq("id", pid).execute()
        data = response.data
        return data[0] if data else None
    
    # Update Project
    def update_project(self, pid, updated_data):
        response = self.client.table("PROJECT").update(updated_data).eq("id", pid).execute()
        data = response.data
        return data[0] if data else None