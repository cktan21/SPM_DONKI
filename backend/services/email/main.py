import smtplib
import os
import asyncio
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from kafka_client import KafkaEventConsumer, EventTypes, Topics
import pytz

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
        logger.info(f"Handling notification event: {event}")
        try:
            event_type = event.get('event_type')
            data = event.get('data', {})
            
            logger.info(f"Processing notification event: {event_type}")
            
            if event_type == EventTypes.DEADLINE_OVERDUE:
                # Handle deadline overdue event
                logger.info(f"Handling deadline overdue event: {data}")
                self._handle_deadline_overdue(data)
            elif event_type == EventTypes.DEADLINE_APPROACHING:
                # Handle deadline approaching event
                logger.info(f"Handling deadline approaching event: {data}")
                self._handle_deadline_approaching(data)
            elif event_type == EventTypes.TASK_ASSIGNED:
                # Handle task assigned event
                logger.info(f"Handling task assigned event: {data}")
                self._handle_task_assigned(data)
            else:
                logger.warning(f"Unknown event type: {event_type}")
                
        except Exception as e:
            logger.error(f"Error handling notification event: {e}")
    
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
    
    def _handle_notification_delivered(self, data: dict):
        """Handle notification delivered events"""
        logger.info(f"Notification delivered: {data}")
        # You can add logic here to update delivery status in database
    
    def _handle_notification_failed(self, data: dict):
        """Handle notification failed events"""
        logger.error(f"Notification failed: {data}")
        # You can add logic here to retry or log failures

async def main():
    """Main function to run the email service as a Kafka consumer"""
    email_service = EmailService()
    consumer = KafkaEventConsumer(
        group_id='email-service-group'  # Unique consumer group for email service
    )
    
    try:
        # Connect to Kafka
        await consumer._connect()
        
        # Subscribe to notification events topic
        await consumer.subscribe_to_topics([Topics.NOTIFICATION_EVENTS])
        
        logger.info("Email service started, listening for notification events...")
        
        # Start consuming events
        await consumer.consume_events(email_service.handle_notification_event)
        
    except KeyboardInterrupt:
        logger.info("Email service stopped by user")
    except Exception as e:
        logger.error(f"Email service error: {e}")
    finally:
        await consumer.close()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
