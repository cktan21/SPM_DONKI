"""
Daily Email Summary Service
Generates and sends daily email summaries to staff members with:
- Tasks due today
- Tasks due tomorrow
- Tasks overdue
- Overall status (Ongoing Tasks)
"""
import os
import logging
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import pytz
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define UTC+8 timezone (Singapore time)
UTC_PLUS_8 = pytz.timezone('Asia/Singapore')

# Service URLs - adjust these based on your deployment
TASK_SERVICE_URL = os.getenv("TASK_SERVICE_URL", "http://localhost:5500")
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:5100")
SCHEDULE_SERVICE_URL = os.getenv("SCHEDULE_SERVICE_URL", "http://localhost:5300")
MANAGE_TASK_SERVICE_URL = os.getenv("MANAGE_TASK_SERVICE_URL", "http://localhost:4100")
PROJECTS_SERVICE_URL = os.getenv("PROJECTS_SERVICE_URL", "http://localhost:5200")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "")


class DailyEmailSummaryService:
    """Service for generating and sending daily email summaries"""
    
    def __init__(self, email_service):
        """
        Initialize the daily email summary service
        
        Args:
            email_service: Instance of EmailService for sending emails
        """
        self.email_service = email_service
    
    def get_all_staff_members(self) -> List[Dict[str, Any]]:
        """
        Fetch all staff members from the user service
        
        Returns:
            List of user dictionaries with id, email, name, department, role
        """
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{USERS_SERVICE_URL}/allUsers")
                if response.status_code == 200:
                    data = response.json()
                    users = data.get("users", [])
                    # Filter for staff members (role: 'staff' or 'manager' or 'hr')
                    staff_members = [
                        user for user in users 
                        if user.get("role", "").lower() in ["staff", "manager", "hr"]
                    ]
                    logger.info(f"Found {len(staff_members)} staff members")
                    return staff_members
                else:
                    logger.error(f"Failed to fetch users: {response.status_code}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching staff members: {e}")
            return []
    
    def get_user_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Fetch all tasks for a user (where user is a collaborator or creator)
        
        Args:
            user_id: User ID to fetch tasks for
            
        Returns:
            List of task dictionaries with schedule information
        """
        all_user_tasks = []
        
        try:
            with httpx.Client(timeout=30.0) as client:
                # 1. Get tasks where user is a collaborator (via composite service)
                try:
                    response = client.get(f"{MANAGE_TASK_SERVICE_URL}/tasks/user/{user_id}")
                    if response.status_code == 200:
                        data = response.json()
                        tasks = data.get("tasks", [])
                        all_user_tasks.extend(tasks)
                        logger.info(f"Found {len(tasks)} tasks where user {user_id} is a collaborator")
                except Exception as e:
                    logger.warning(f"Error fetching collaborator tasks: {e}")
                
                # 2. Get tasks where user is the creator
                try:
                    # Get all tasks and filter by created_by_uid
                    response = client.get(f"{TASK_SERVICE_URL}/tasks")
                    if response.status_code == 200:
                        data = response.json()
                        all_tasks = data.get("tasks", [])
                        
                        # Filter tasks created by this user
                        creator_tasks = [
                            task for task in all_tasks 
                            if task.get("created_by_uid") == user_id
                        ]
                        
                        # Enrich creator tasks with schedule and project data
                        for task in creator_tasks:
                            task_id = task.get("id")
                            
                            # Get schedule data
                            try:
                                schedule_response = client.get(
                                    f"{SCHEDULE_SERVICE_URL}/tid/{task_id}/latest"
                                )
                                if schedule_response.status_code == 200:
                                    schedule_data = schedule_response.json().get("data", {})
                                    task["status"] = schedule_data.get("status")
                                    task["deadline"] = schedule_data.get("deadline")
                            except Exception:
                                pass
                            
                            # Get project data
                            try:
                                project_id = task.get("pid")
                                if project_id:
                                    project_response = client.get(
                                        f"{PROJECTS_SERVICE_URL}/pid/{project_id}"
                                    )
                                    if project_response.status_code == 200:
                                        project_data = project_response.json().get("project", {})
                                        task["project"] = project_data
                            except Exception:
                                pass
                        
                        # Add creator tasks that aren't already in the list
                        existing_task_ids = {t.get("id") for t in all_user_tasks}
                        new_creator_tasks = [
                            t for t in creator_tasks 
                            if t.get("id") not in existing_task_ids
                        ]
                        all_user_tasks.extend(new_creator_tasks)
                        logger.info(f"Found {len(new_creator_tasks)} additional tasks where user {user_id} is the creator")
                        
                except Exception as e:
                    logger.warning(f"Error fetching creator tasks: {e}")
                
                logger.info(f"Total tasks found for user {user_id}: {len(all_user_tasks)}")
                return all_user_tasks
                
        except Exception as e:
            logger.error(f"Error fetching tasks for user {user_id}: {e}")
            return []
    
    def categorize_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Categorize tasks into: due_today, due_tomorrow, overdue, ongoing
        
        Args:
            tasks: List of task dictionaries with deadline information
            
        Returns:
            Dictionary with categorized task lists
        """
        now = datetime.now(UTC_PLUS_8)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        tomorrow_end = today_end + timedelta(days=1)
        
        categorized = {
            "due_today": [],
            "due_tomorrow": [],
            "overdue": [],
            "ongoing": []
        }
        
        for task in tasks:
            deadline_str = task.get("deadline")
            status = task.get("status", "").lower()
            
            # Skip tasks without deadlines or completed tasks
            if not deadline_str:
                # Include tasks without deadlines in ongoing if status is ongoing
                if status == "ongoing":
                    categorized["ongoing"].append(task)
                continue
            
            try:
                # Parse deadline
                deadline_dt = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                if deadline_dt.tzinfo is None:
                    deadline_dt = UTC_PLUS_8.localize(deadline_dt)
                else:
                    deadline_dt = deadline_dt.astimezone(UTC_PLUS_8)
                
                # Categorize based on deadline
                if deadline_dt < today_start:
                    # Overdue
                    if status != "completed":
                        categorized["overdue"].append(task)
                elif today_start <= deadline_dt < today_end:
                    # Due today
                    if status != "completed":
                        categorized["due_today"].append(task)
                elif today_end <= deadline_dt < tomorrow_end:
                    # Due tomorrow
                    if status != "completed":
                        categorized["due_tomorrow"].append(task)
                
                # Add to ongoing if status is ongoing (regardless of deadline)
                if status == "ongoing":
                    categorized["ongoing"].append(task)
                    
            except Exception as e:
                logger.warning(f"Error parsing deadline for task {task.get('id')}: {e}")
                # If we can't parse deadline but status is ongoing, include it
                if status == "ongoing":
                    categorized["ongoing"].append(task)
        
        # Remove duplicates from ongoing (tasks might appear in multiple categories)
        seen_ids = set()
        unique_ongoing = []
        for task in categorized["ongoing"]:
            task_id = task.get("id")
            if task_id and task_id not in seen_ids:
                seen_ids.add(task_id)
                unique_ongoing.append(task)
        categorized["ongoing"] = unique_ongoing
        
        return categorized
    
    def format_task_list(self, tasks: List[Dict[str, Any]], max_tasks: int = 10) -> str:
        """
        Format a list of tasks for email display
        
        Args:
            tasks: List of task dictionaries
            max_tasks: Maximum number of tasks to display
            
        Returns:
            Formatted string of tasks
        """
        if not tasks:
            return "  None\n"
        
        formatted = ""
        display_tasks = tasks[:max_tasks]
        
        for task in display_tasks:
            task_name = task.get("name", "Unnamed Task")
            task_id = task.get("id", "N/A")
            deadline_str = task.get("deadline", "No deadline")
            priority = task.get("priorityLevel", "N/A")
            project_name = task.get("project", {}).get("name", "Unknown Project") if isinstance(task.get("project"), dict) else "Unknown Project"
            
            # Format deadline
            deadline_display = deadline_str
            if deadline_str and deadline_str != "No deadline":
                try:
                    deadline_dt = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                    if deadline_dt.tzinfo is None:
                        deadline_dt = UTC_PLUS_8.localize(deadline_dt)
                    else:
                        deadline_dt = deadline_dt.astimezone(UTC_PLUS_8)
                    deadline_display = deadline_dt.strftime('%Y-%m-%d %H:%M UTC+8')
                except:
                    pass
            
            formatted += f"  • {task_name}\n"
            formatted += f"    Project: {project_name} | Priority: {priority} | Deadline: {deadline_display}\n"
        
        if len(tasks) > max_tasks:
            formatted += f"  ... and {len(tasks) - max_tasks} more task(s)\n"
        
        return formatted
    
    def generate_email_body(self, user_name: str, categorized_tasks: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Generate the email body for daily summary
        
        Args:
            user_name: Name of the user
            categorized_tasks: Dictionary with categorized task lists
            
        Returns:
            Formatted email body string
        """
        today = datetime.now(UTC_PLUS_8).strftime('%Y-%m-%d')
        
        body = f"""Hello {user_name},

Here is your daily task summary for {today}:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 OVERDUE TASKS ({len(categorized_tasks['overdue'])})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.format_task_list(categorized_tasks['overdue'])}

📅 TASKS DUE TODAY ({len(categorized_tasks['due_today'])})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.format_task_list(categorized_tasks['due_today'])}

📆 TASKS DUE TOMORROW ({len(categorized_tasks['due_tomorrow'])})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.format_task_list(categorized_tasks['due_tomorrow'])}

📊 ONGOING TASKS ({len(categorized_tasks['ongoing'])})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.format_task_list(categorized_tasks['ongoing'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
  • Overdue: {len(categorized_tasks['overdue'])} task(s)
  • Due Today: {len(categorized_tasks['due_today'])} task(s)
  • Due Tomorrow: {len(categorized_tasks['due_tomorrow'])} task(s)
  • Ongoing: {len(categorized_tasks['ongoing'])} task(s)

Please check your dashboard for more details and to update your task status.

Best regards,
Project Management System
"""
        return body
    
    def send_daily_summary_to_user(self, user: Dict[str, Any]) -> bool:
        """
        Generate and send daily summary email to a single user
        
        Args:
            user: User dictionary with id, email, name, etc.
            
        Returns:
            True if email sent successfully, False otherwise
        """
        user_id = user.get("id")
        user_email = user.get("email")
        user_name = user.get("name", "Staff Member")
        
        if not user_id or not user_email:
            logger.warning(f"Skipping user with missing id or email: {user}")
            return False
        
        try:
            # Fetch user's tasks
            tasks = self.get_user_tasks(user_id)
            
            if not tasks:
                logger.info(f"No tasks found for user {user_id}, skipping email")
                return False
            
            # Categorize tasks
            categorized_tasks = self.categorize_tasks(tasks)
            
            # Check if user has any relevant tasks
            total_relevant = (
                len(categorized_tasks['overdue']) +
                len(categorized_tasks['due_today']) +
                len(categorized_tasks['due_tomorrow']) +
                len(categorized_tasks['ongoing'])
            )
            
            if total_relevant == 0:
                logger.info(f"No relevant tasks for user {user_id}, skipping email")
                return False
            
            # Generate email
            subject = f"Daily Task Summary - {datetime.now(UTC_PLUS_8).strftime('%Y-%m-%d')}"
            body = self.generate_email_body(user_name, categorized_tasks)
            
            # Send email
            success = self.email_service.send_email(user_email, subject, body)
            
            if success:
                logger.info(f"✅ Daily summary sent to {user_email}")
            else:
                logger.error(f"❌ Failed to send daily summary to {user_email}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending daily summary to user {user_id}: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def send_daily_summaries(self):
        """
        Send daily email summaries to all staff members
        This method is called by the scheduler
        """
        logger.info("📧 Starting daily email summary job...")
        start_time = datetime.now(UTC_PLUS_8)
        
        # Get all staff members
        staff_members = self.get_all_staff_members()
        
        if not staff_members:
            logger.warning("No staff members found, skipping daily summaries")
            return
        
        logger.info(f"Processing {len(staff_members)} staff members...")
        
        # Send summary to each staff member
        success_count = 0
        failure_count = 0
        
        for user in staff_members:
            if self.send_daily_summary_to_user(user):
                success_count += 1
            else:
                failure_count += 1
        
        end_time = datetime.now(UTC_PLUS_8)
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"✅ Daily email summary job completed in {duration:.2f}s")
        logger.info(f"   Success: {success_count}, Failed: {failure_count}")

