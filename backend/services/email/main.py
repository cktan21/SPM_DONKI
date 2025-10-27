import smtplib
import os
import asyncio
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from kafka_client import KafkaEventConsumer, EventTypes, Topics

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            else:
                logger.warning(f"Unknown event type: {event_type}")
                
        except Exception as e:
            logger.error(f"Error handling notification event: {e}")
    
    def _handle_deadline_overdue(self, data: dict):
        """Handle notification sent events"""
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
