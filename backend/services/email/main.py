import smtplib
import os
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from kafka_client import KafkaEventConsumer, EventTypes, Topics
import pytz
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from daily_email_summary import DailyEmailSummaryService

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define UTC+8 timezone (Singapore time)
UTC_PLUS_8 = pytz.timezone('Asia/Singapore')

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_pass = os.getenv("SMTP_PASS")
        
        if not all([self.smtp_server, self.smtp_port, self.smtp_user, self.smtp_pass]):
            raise ValueError("Missing SMTP configuration. Check your .env file.")
    
    def send_email(self, to_email: str, subject: str, body: str):
        """Send email via SMTP"""
        logger.info(f"Sending email to: {to_email}")
        
        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_pass)
            server.sendmail(self.smtp_user, to_email, msg.as_string())
            server.quit()
            logger.info("✅ Email sent successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False
    
    def handle_notification_event(self, event: dict):
        """Handle incoming notification events from Kafka"""
        logger.info(f"📧 Handling notification event: {event}")
        try:
            event_type = event.get('event_type')
            data = event.get('data', {})
            
            logger.info(f"📋 Processing notification event: {event_type}")
            logger.info(f"📊 Event data: {data}")
            
            if event_type == EventTypes.DEADLINE_OVERDUE:
                # Handle deadline overdue event
                logger.info(f"⏰ Handling deadline overdue event: {data}")
                self._handle_deadline_overdue(data)
            elif event_type == EventTypes.DEADLINE_APPROACHING:
                # Handle deadline approaching event
                logger.info(f"⏰ Handling deadline approaching event: {data}")
                self._handle_deadline_approaching(data)
            elif event_type == EventTypes.TASK_ASSIGNED:
                # Handle task assigned event
                logger.info(f"📝 Handling task assigned event: {data}")
                self._handle_task_assigned(data)
            elif event_type == EventTypes.PROJECT_COLLABORATOR_ADDED:
                # Handle project collaborator added event
                logger.info(f"👥 Handling project collaborator added event: {data}")
                self._handle_project_collaborator_added(data)
            elif event_type == EventTypes.TASK_DELETED:
                # Handle task deleted event
                logger.info(f"🗑️ Handling task deleted event: {data}")
                self._handle_task_deleted(data)
            elif event_type == EventTypes.TASK_UPDATED:
                # Handle task updated event
                logger.info(f"📝 Handling task updated event: {data}")
                self._handle_task_updated(data)
            else:
                logger.warning(f"❓ Unknown event type: {event_type}")
                
        except Exception as e:
            logger.error(f"❌ Error handling notification event: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
    
    def _handle_deadline_overdue(self, data: dict):
        """Handle deadline overdue events"""
        # Extract email details from the event data
        to_email = data.get('email')
        name = data.get('name')
        task_id = data.get('tid')
        department = data.get('department')
        subject = data.get('subject', f"Deadline Overdue for Task {task_id} from Department {department}")
        body = data.get('body', f'Hello {name} of Department {department}, your task {task_id} is Overdue! 🚨🚨🚨🚨 Do it Soon!!')
        
        if to_email:
            self.send_email(to_email, subject, body)
        else:
            logger.warning("No email address provided in notification data")
    
    def _handle_deadline_approaching(self, data: dict):
        """Handle deadline approaching events"""
        # Extract email details from the event data
        to_email = data.get('email')
        name = data.get('name')
        task_id = data.get('tid')
        department = data.get('department')
        deadline = data.get('deadline')
        
        # Format deadline for display in UTC+8
        deadline_display = deadline
        if deadline:
            try:
                deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
                # Convert to UTC+8 timezone
                if deadline_dt.tzinfo is None:
                    deadline_dt = UTC_PLUS_8.localize(deadline_dt)
                else:
                    deadline_dt = deadline_dt.astimezone(UTC_PLUS_8)
                deadline_display = deadline_dt.strftime('%Y-%m-%d %H:%M:%S UTC+8')
            except:
                pass
        
        subject = data.get('subject', f"Deadline Approaching for Task {task_id} from Department {department}")
        body = data.get('body', f'Hello {name} of Department {department}, your task {task_id} deadline is approaching! ⏰⏰⏰ The deadline is on {deadline_display}. Please make sure to complete it on time!')
        
        if to_email:
            self.send_email(to_email, subject, body)
        else:
            logger.warning("No email address provided in notification data")
    
    def _handle_task_assigned(self, data: dict):
        """Handle task assigned events"""
        # Extract email details from the event data
        to_email = data.get('email')
        name = data.get('name')
        task_id = data.get('tid')
        task_name = data.get('task_name', 'Unknown Task')
        department = data.get('department')
        is_creator = data.get('is_creator', False)
        is_collaborator = data.get('is_collaborator', False)
        
        # Determine role and message
        if is_creator:
            role_text = "You have been assigned as the creator"
            action_text = "created"
        elif is_collaborator:
            role_text = "You have been assigned as a collaborator"
            action_text = "assigned to collaborate on"
        else:
            role_text = "You have been assigned to"
            action_text = "assigned to"
        
        subject = data.get('subject', f"New Task Assignment: {task_name}")
        body = data.get('body', f'Hello {name} of Department {department}, {role_text} for task "{task_name}" (ID: {task_id}). You have been {action_text} this task. Please check your dashboard for more details.')
        
        if to_email:
            self.send_email(to_email, subject, body)
        else:
            logger.warning("No email address provided in notification data")
    
    def _handle_project_collaborator_added(self, data: dict):
        """Handle project collaborator added events"""
        # Extract email details from the event data
        to_email = data.get('email')
        name = data.get('name')
        project_id = data.get('project_id')
        project_name = data.get('project_name', 'Unknown Project')
        department = data.get('department')
        added_by_name = data.get('added_by_name', 'System')
        task_name = data.get('task_name', 'Unknown Task')
        
        subject = data.get('subject', f"Added to Project: {project_name}")
        body = data.get('body', f'Hello {name} of Department {department},\n\nYou have been added as a member to the project "{project_name}" (ID: {project_id}) because you are involved in the task "{task_name}".\n\nThis means you now have access to all project resources and will receive updates about project activities.\n\nAdded by: {added_by_name}\n\nPlease check your dashboard for more project details.\n\nBest regards,\nProject Management System')
        
        if to_email:
            self.send_email(to_email, subject, body)
        else:
            logger.warning("No email address provided in project collaborator notification data")
    
    def _handle_task_deleted(self, data: dict):
        """Handle task deleted events"""
        # Extract email details from the event data
        to_email = data.get('email')
        name = data.get('name')
        task_id = data.get('tid')
        task_name = data.get('task_name', 'Unknown Task')
        department = data.get('department')
        # deleted_by_name = data.get('deleted_by_name', 'System')
        project_name = data.get('project_name', 'Unknown Project')
        
        subject = data.get('subject', f"Task Deleted: {task_name}")
        body = data.get('body', f'Hello {name} of Department {department},\n\nTask "{task_name}" (ID: {task_id}) from project "{project_name}" has been deleted.\n\nThis task is no longer available and has been removed from your task list.\n\nIf you have any questions about this deletion, please contact your project manager.\n\nBest regards,\nProject Management System')
        
        if to_email:
            self.send_email(to_email, subject, body)
        else:
            logger.warning("No email address provided in task deletion notification data")
    
    def _handle_task_updated(self, data: dict):
        """Handle task updated events"""
        # Extract email details from the event data
        to_email = data.get('email')
        name = data.get('name')
        task_id = data.get('tid')
        task_name = data.get('task_name', 'Unknown Task')
        department = data.get('department')
        # updated_by_name = data.get('updated_by_name', 'System')
        project_name = data.get('project_name', 'Unknown Project')
        changes = data.get('changes', {})
        
        # Build changes description
        changes_text = ""
        if changes:
            changes_list = []
            if 'status' in changes:
                changes_list.append(f"Status: {changes['status']}")
            if 'priority' in changes:
                changes_list.append(f"Priority: {changes['priority']}")
            if 'deadline' in changes:
                changes_list.append(f"Deadline: {changes['deadline']}")
            if 'description' in changes:
                changes_list.append("Description updated")
            if 'title' in changes:
                changes_list.append("Title updated")
            
            if changes_list:
                changes_text = f"\n\nChanges made:\n" + "\n".join(f"• {change}" for change in changes_list)
        
        subject = data.get('subject', f"Task Updated: {task_name}")
        body = data.get('body', f'Hello {name} of Department {department},\n\nTask "{task_name}" (ID: {task_id}) from project "{project_name}" has been updated.{changes_text}\n\nPlease check your dashboard for the latest task details.\n\nBest regards,\nProject Management System')
        
        if to_email:
            self.send_email(to_email, subject, body)
        else:
            logger.warning("No email address provided in task update notification data")
    
    def _handle_notification_delivered(self, data: dict):
        """Handle notification delivered events"""
        logger.info(f"Notification delivered: {data}")
        # You can add logic here to update delivery status in database
    
    def _handle_notification_failed(self, data: dict):
        """Handle notification failed events"""
        logger.error(f"Notification failed: {data}")
        # You can add logic here to retry or log failures

def setup_daily_email_scheduler(email_service: EmailService):
    """
    Setup and start the daily email summary scheduler
    Sends daily summaries at 8:15 AM UTC+8 (Singapore time)
    """
    try:
        # Initialize daily email summary service
        daily_summary_service = DailyEmailSummaryService(email_service)
        
        # Create scheduler
        scheduler = BackgroundScheduler(timezone=UTC_PLUS_8)
        
        # Schedule daily email summary at 8:15 AM UTC+8
        scheduler.add_job(
            func=daily_summary_service.send_daily_summaries,
            trigger=CronTrigger(hour=8, minute=15, timezone=UTC_PLUS_8),
            id='daily_email_summary',
            name='Daily Email Summary at 8:15 AM',
            replace_existing=True
        )
        
        # Start scheduler
        scheduler.start()
        logger.info("✅ Daily email summary scheduler started")
        logger.info("📅 Daily summaries will be sent at 8:15 AM UTC+8 (Singapore time)")
        
        return scheduler
    except Exception as e:
        logger.error(f"❌ Failed to setup daily email scheduler: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return None

def main():
    """Main function to run the email service as a Kafka consumer"""
    email_service = EmailService()
    consumer = KafkaEventConsumer(
        group_id='email-service-group'  # Unique consumer group for email service
    )
    
    # Setup daily email summary scheduler
    scheduler = setup_daily_email_scheduler(email_service)
    
    try:
        # Connect to Kafka
        logger.info("🔌 Connecting to Kafka...")
        consumer._connect()
        
        # Subscribe to notification events topic
        logger.info(f"📡 Subscribing to topic: {Topics.NOTIFICATION_EVENTS}")
        success = consumer.subscribe_to_topics([Topics.NOTIFICATION_EVENTS])
        
        if not success:
            logger.error("❌ Failed to subscribe to topics")
            return
        
        logger.info("✅ Email service started, waiting for notification events...")
        logger.info("⏳ Topic will be created automatically when first message is published")
        
        # Start consuming events (will wait for topic creation)
        consumer.consume_events(email_service.handle_notification_event)
        
    except KeyboardInterrupt:
        logger.info("🛑 Email service stopped by user")
    except Exception as e:
        logger.error(f"❌ Email service error: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
    finally:
        if scheduler:
            scheduler.shutdown()
        consumer.close()

if __name__ == "__main__":
    import sys
    
    # Check if manual trigger is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--send-daily-summary":
        # Manual trigger for testing daily summaries
        logger.info("📧 Manually triggering daily email summary...")
        email_service = EmailService()
        daily_summary_service = DailyEmailSummaryService(email_service)
        daily_summary_service.send_daily_summaries()
        logger.info("✅ Daily summary job completed")
    else:
        # Run the main function (Kafka consumer + scheduler)
        main()
