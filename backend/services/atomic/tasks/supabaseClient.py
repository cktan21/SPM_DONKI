from supabase import create_client, Client
import os

# Class to Add the Supabase Client
class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_API_KEY")
        self.client: Client = create_client(self.url, self.key)
    
    def get_all_tasks(self, filter_by: dict = None):
        """
        Fetch all tasks from TASK table.
        Optional filter_by: dictionary with column:value pairs for filtering
        """
        query = self.client.table("TASK").select("*")
        
        if filter_by:
            for key, value in filter_by.items():
                query = query.eq(key, value)
        
        resp = query.execute()
        return getattr(resp, "data", None) or []

    def update_task(self, task_id, updates):
        """Update a task with the provided data and return the updated row"""
        # Perform the update
        response = (
            self.client
            .table("TASK")
            .update(updates)
            .eq("id", task_id)
            .execute()
        )

        # If the update response doesn’t include the row, fetch it explicitly
        if not getattr(response, "data", None):
            response = (
                self.client
                .table("TASK")
                .select("*")
                .eq("id", task_id)
                .execute()
            )

        return response
    
    def delete_task(self, task_id: str):
        """Delete a task by its ID (ignores ownership)."""
        response = (
            self.client
            .table("TASK")
            .delete()
            .eq("id", task_id)
            .execute()
        )
        return response