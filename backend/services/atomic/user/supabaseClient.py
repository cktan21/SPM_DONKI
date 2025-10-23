from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from the .env file in the same folder
load_dotenv(dotenv_path="./.env")  # adjust path if needed

# Class to Add the Supabase Client
class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.client: Client = create_client(self.url, self.key)
    
    # Authentication Methods
    def sign_in_with_password(self, email: str, password: str):
        """Authenticate user with email and password"""
        return self.client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    
    def sign_up(self, email: str, password: str, role: str = "user", name: str = "New User", department: str = "General"):
        """Create new user account"""
        return self.client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "role": role,
                    "name": name,
                    "department": department,
                }
            }
        })
    
    def set_session(self, access_token: str, refresh_token: str):
        """Set session with access and refresh tokens"""
        return self.client.auth.set_session(access_token, refresh_token)
    
    def sign_out(self, scope: str = 'local'):
        """Sign out user"""
        return self.client.auth.sign_out(scope=scope)
    
    def refresh_session(self, refresh_token: str):
        """Refresh access token using refresh token"""
        return self.client.auth.refresh_session(refresh_token)
    
    # User Data Methods
    def get_user_by_auth_id(self, auth_id: str):
        """Get user data by auth_id"""
        response = self.client.table("USER").select(
            "id, email, role, name", "department"
        ).eq("auth_id", auth_id).execute()
        return response
    
    def get_user_by_id(self, user_id: str):
        """Get user data by user ID"""
        response = self.client.table("USER").select(
            "id, auth_id, email, role, name, created_at", "department"
        ).eq("id", user_id).execute()
        return response
    
    def get_all_users(self):
        """Get all users"""
        response = self.client.table("USER").select("*").execute()
        return response.data if response.data else []