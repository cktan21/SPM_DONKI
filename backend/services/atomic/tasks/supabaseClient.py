from supabase import create_client, Client
import os

# Class to Add the Supabase Client
class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_API_KEY")
        self.client: Client = create_client(self.url, self.key)
    
    # Sample Code PLS CHANGE
    def insert_recommendation(self, rec):
        response = self.client.table("Recommendations").insert({
            "uuid": rec.id,
            "recommendation": rec.recommendations
        }).execute()
        return response

    def fetch_recommendation(self, id):
        response = self.client.table("Recommendations").select("*").eq("uuid", id).execute()
        data = response.data
        return data[0] if data else None