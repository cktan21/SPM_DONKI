from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from dateutil.relativedelta import relativedelta
from schedule_client import ScheduleClient
import logging
import pytz
import requests
from kafka_client import EventTypes, KafkaEventPublisher, Topics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define UTC+8 timezone (Singapore time)
UTC_PLUS_8 = pytz.timezone('Asia/Singapore')

class RecurringTaskProcessor:
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=UTC_PLUS_8)
        self.schedule_client = ScheduleClient()
        self.kafka_publisher = KafkaEventPublisher()
        self.scheduler.start()
        logger.info("RecurringTaskProcessor initialized and scheduler started with UTC+8 timezone")
    
    def initialize_kafka(self):
        """
        Initialize Kafka producer connection
        """
        try:
            self.kafka_publisher._connect()
            logger.info("Kafka producer initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            return False

    def calculate_next_occurrence(self, frequency: str, current_start: datetime, current_deadline: datetime) -> datetime:
        """
        Calculate the next occurrence based on frequency and the gap between start and deadline
        """
        # Ensure both datetimes are in UTC+8 timezone
        if current_start.tzinfo is None:
            current_start = UTC_PLUS_8.localize(current_start)
        else:
            current_start = current_start.astimezone(UTC_PLUS_8)
            
        if current_deadline.tzinfo is None:
            current_deadline = UTC_PLUS_8.localize(current_deadline)
        else:
            current_deadline = current_deadline.astimezone(UTC_PLUS_8)
        
        # Calculate the gap between start and deadline
        gap = current_deadline - current_start
        
        if frequency == "Weekly":
            # Add 1 week to the current start time
            next_start = current_start + timedelta(weeks=1)
            return next_start + gap
            
        elif frequency == "Monthly":
            # Add 1 month to the current start time using relativedelta to handle day overflow
            next_start = current_start + relativedelta(months=1)
            return next_start + gap
            
        elif frequency == "Yearly":
            # Add 1 year to the current start time using relativedelta
            next_start = current_start + relativedelta(years=1)
            return next_start + gap
            
        elif frequency == "Immediate":
            # For immediate, create the next occurrence right after the current deadline
            return current_deadline + timedelta(minutes=1)
            
        else:
            raise ValueError(f"Unsupported frequency: {frequency}")

    def create_recurring_entry(self, original_entry: Dict[str, Any], frequency: str) -> Optional[Dict[str, Any]]:
        """
        Create a new recurring entry based on the original entry and frequency
        """
        try:
            # Parse the original entry data
            tid = original_entry["tid"]
            original_start = datetime.fromisoformat(original_entry["start"].replace('Z', '+00:00'))
            original_deadline = datetime.fromisoformat(original_entry["deadline"].replace('Z', '+00:00'))
            
            # Calculate new start and deadline times
            new_start = self.calculate_next_occurrence(frequency, original_start, original_deadline)
            new_deadline = new_start + (original_deadline - original_start)
            
            # Calculate next occurrence for the new entry
            next_occurrence = self.calculate_next_occurrence(frequency, new_start, new_deadline)
            
            # Create new schedule entry via schedule service
            new_entry = self.schedule_client.create_schedule(
                tid=tid,
                start=new_start.isoformat(),
                deadline=new_deadline.isoformat(),
                is_recurring=True,
                status="ongoing",
                next_occurrence=next_occurrence.isoformat(),
                frequency=frequency
            )
            
            logger.info(f"Created new recurring entry for task {tid} with frequency {frequency}")
            return new_entry
            
        except Exception as e:
            logger.error(f"Error creating recurring entry: {str(e)}")
            return None

    def schedule_recurring_task(self, task_data: Dict[str, Any]):
        """
        Schedule a recurring task to be processed at the next occurrence time
        """
        try:
            sid = task_data.get("sid")
            frequency = task_data.get("frequency")
            next_occurrence_str = task_data.get("next_occurrence")
            
            if not all([sid, frequency, next_occurrence_str]):
                logger.error(f"Missing required fields for task {sid}")
                return False
            
            # Parse the next occurrence datetime
            next_occurrence_dt = datetime.fromisoformat(next_occurrence_str.replace('Z', '+00:00'))
            
            # Schedule the job to run at the next occurrence time
            job_id = f"recurring_{sid}"
            self.scheduler.add_job(
                func=self.process_recurring_task,
                trigger=DateTrigger(run_date=next_occurrence_dt),
                args=[sid, frequency],
                id=job_id,
                replace_existing=True
            )
            
            logger.info(f"Scheduled recurring task {sid} for {next_occurrence_dt} with frequency {frequency}")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling recurring task {sid}: {str(e)}")
            return False

    def schedule_deadline_monitoring(self, task_data: Dict[str, Any]):
        """
        Schedule deadline monitoring jobs for a task (approaching and overdue)
        """
        try:
            sid = task_data.get("sid")
            deadline_str = task_data.get("deadline")
            
            if not all([sid, deadline_str]):
                logger.error(f"Missing required fields for deadline monitoring {sid}")
                return False
            
            # Parse the deadline datetime and ensure it's in UTC+8
            deadline_dt = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
            if deadline_dt.tzinfo is None:
                deadline_dt = UTC_PLUS_8.localize(deadline_dt)
            else:
                deadline_dt = deadline_dt.astimezone(UTC_PLUS_8)
            
            # Calculate approaching notification time (3 days before deadline)
            approaching_dt = deadline_dt - timedelta(days=3)
            
            # Get current time in UTC+8
            current_time = datetime.now(UTC_PLUS_8)
            
            # Only schedule approaching notification if it's in the future
            if approaching_dt > current_time:
                # Schedule the deadline approaching job
                approaching_job_id = f"deadline_approaching_{sid}"
                self.scheduler.add_job(
                    func=self.process_deadline_approaching,
                    trigger=DateTrigger(run_date=approaching_dt),
                    args=[sid],
                    id=approaching_job_id,
                    replace_existing=True
                )
                logger.info(f"Scheduled deadline approaching notification for task {sid} at {approaching_dt} (UTC+8)")
            
            # Schedule the deadline overdue job
            overdue_job_id = f"deadline_{sid}"
            self.scheduler.add_job(
                func=self.process_deadline_reached,
                trigger=DateTrigger(run_date=deadline_dt),
                args=[sid],
                id=overdue_job_id,
                replace_existing=True
            )
            
            logger.info(f"Scheduled deadline monitoring for task {sid} at {deadline_dt} (UTC+8)")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling deadline monitoring for {sid}: {str(e)}")
            return False

    def process_deadline_approaching(self, sid: str):
        """
        Process when a task deadline is approaching (3 days before) - broadcast to Kafka
        """
        try:
            logger.info(f"Processing deadline approaching for task {sid}")
            
            # Get the current schedule entry
            current_entry = self.schedule_client.fetch_schedule_by_sid(sid)
            if not current_entry:
                logger.error(f"Schedule entry {sid} not found for deadline approaching processing")
                return False
            
            logger.info(f"Current schedule entry for {sid}: {current_entry}")
            
            # Get task name from task service
            task_name = "Unknown Task"
            tid = current_entry.get("tid")
            if tid:
                try:
                    task_response = requests.get(f"{self.schedule_client.task_service_url}/tid/{tid}", timeout=5)
                    if task_response.status_code == 200:
                        task_data = task_response.json().get("task", {})
                        task_name = task_data.get("name", "Unknown Task")
                        logger.info(f"Fetched task name for {tid}: {task_name}")
                except Exception as e:
                    logger.warning(f"Could not fetch task name for {tid}: {e}")
            
            # Broadcast deadline approaching event to Kafka
            event_data = {
                "sid": sid,
                "tid": tid,
                "task_name": task_name,
                "deadline": current_entry.get("deadline"),
                "status": "approaching",
                "timestamp": datetime.now(UTC_PLUS_8).isoformat()
            }
            
            # Call sid and then task to get the user info
            user_info = self.schedule_client.get_user_info(sid)
            if not user_info:
                logger.error(f"Task info not found for {sid}")
                return False
            
            # Broadcast events synchronously
            return self._broadcast_deadline_approaching_events(user_info, event_data)
                
        except Exception as e:
            logger.error(f"Error processing deadline approaching for {sid}: {str(e)}")
            return False

    def process_deadline_reached(self, sid: str):
        """
        Process when a task deadline is reached - broadcast to Kafka and update status
        """
        try:
            logger.info(f"Processing deadline reached for task {sid}")
            
            # Get the current schedule entry
            current_entry = self.schedule_client.fetch_schedule_by_sid(sid)
            if not current_entry:
                logger.error(f"Schedule entry {sid} not found for deadline processing")
                return False
            
            logger.info(f"Current schedule entry for {sid}: {current_entry}")
            
            # Update task status to "overdue" via schedule service
            logger.info(f"Attempting to update schedule {sid} status to 'overdue'")
            update_success = self.schedule_client.update_schedule(sid, {"status": "overdue"})
            logger.info(f"Schedule update result for {sid}: {update_success}")
            
            if not update_success:
                logger.error(f"Failed to update task status to overdue for {sid}")
                return False
            
            # Get task name from task service
            task_name = "Unknown Task"
            tid = current_entry.get("tid")
            if tid:
                try:
                    task_response = requests.get(f"{self.schedule_client.task_service_url}/tid/{tid}", timeout=5)
                    if task_response.status_code == 200:
                        task_data = task_response.json().get("task", {})
                        task_name = task_data.get("name", "Unknown Task")
                        logger.info(f"Fetched task name for {tid}: {task_name}")
                except Exception as e:
                    logger.warning(f"Could not fetch task name for {tid}: {e}")
            
            # Broadcast deadline overdue event to Kafka
            event_data = {
                "sid": sid,
                "tid": tid,
                "task_name": task_name,
                "deadline": current_entry.get("deadline"),
                "status": "overdue",
                "timestamp": datetime.now(UTC_PLUS_8).isoformat()
            }
            
            # Call sid and then task to get the user info
            user_info = self.schedule_client.get_user_info(sid)
            if not user_info:
                logger.error(f"Task info not found for {sid}")
                return False
            
            # Broadcast events synchronously
            return self._broadcast_deadline_events(user_info, event_data)
                
        except Exception as e:
            logger.error(f"Error processing deadline reached for {sid}: {str(e)}")
            return False

    def _broadcast_deadline_approaching_events(self, user_info, event_data) -> bool:
        """
        Broadcast deadline approaching events to all users synchronously
        """
        try:
            # Ensure Kafka producer is connected
            if not self.kafka_publisher.producer:
                self.kafka_publisher._connect()
            
            # Send events to all users
            failed_count = 0
            success_count = 0
            
            for user in user_info:
                local_event_data = event_data.copy()
                local_event_data["uid"] = user.get("user_id")
                local_event_data["name"] = user.get("user_name")
                local_event_data["email"] = user.get("user_email")
                local_event_data["role"] = user.get("user_role")
                local_event_data["department"] = user.get("department")
                
                # Publish event synchronously
                success = self.kafka_publisher.publish_event(
                    topic=Topics.NOTIFICATION_EVENTS,
                    event_type=EventTypes.DEADLINE_APPROACHING,
                    data=local_event_data,
                )
                
                if success:
                    success_count += 1
                else:
                    failed_count += 1
                    logger.error(f"Failed to broadcast deadline approaching event for user {user.get('user_id')}")
            
            if failed_count > 0:
                logger.error(f"Failed to broadcast {failed_count} out of {len(user_info)} deadline approaching events")
                return False
            
            logger.info(f"Successfully broadcasted deadline approaching events for {success_count} users")
            return True
            
        except Exception as e:
            logger.error(f"Error broadcasting deadline approaching events: {str(e)}")
            return False

    def _broadcast_deadline_events(self, user_info, event_data) -> bool:
        """
        Broadcast deadline overdue events to all users synchronously
        """
        try:
            # Ensure Kafka producer is connected
            if not self.kafka_publisher.producer:
                self.kafka_publisher._connect()
            
            # Send events to all users
            failed_count = 0
            success_count = 0
            
            for user in user_info:
                local_event_data = event_data.copy()
                local_event_data["uid"] = user.get("user_id")
                local_event_data["name"] = user.get("user_name")
                local_event_data["email"] = user.get("user_email")
                local_event_data["role"] = user.get("user_role")
                local_event_data["department"] = user.get("department")
                
                # Publish event synchronously
                success = self.kafka_publisher.publish_event(
                    topic=Topics.NOTIFICATION_EVENTS,
                    event_type=EventTypes.DEADLINE_OVERDUE,
                    data=local_event_data,
                )
                
                if success:
                    success_count += 1
                else:
                    failed_count += 1
                    logger.error(f"Failed to broadcast deadline overdue event for user {user.get('user_id')}")
            
            if failed_count > 0:
                logger.error(f"Failed to broadcast {failed_count} out of {len(user_info)} deadline overdue events")
                return False
            
            logger.info(f"Successfully broadcasted deadline overdue events for {success_count} users")
            return True
            
        except Exception as e:
            logger.error(f"Error broadcasting deadline events: {str(e)}")
            return False

    def process_recurring_task(self, sid: str, frequency: str):
        """
        Process a recurring task when its next occurrence time is reached
        """
        try:
            logger.info(f"Processing recurring task {sid} with frequency {frequency}")
            
            # Get the current schedule entry via schedule service
            current_entry = self.schedule_client.fetch_schedule_by_sid(sid)
            if not current_entry:
                logger.error(f"Schedule entry {sid} not found")
                return
            
            # Create new recurring entry
            new_entry = self.create_recurring_entry(current_entry, frequency)
            if new_entry:
                logger.info(f"Successfully created new recurring entry for task {current_entry['tid']}")
                
                # Schedule the next occurrence for the new entry
                new_sid = new_entry["sid"]
                new_next_occurrence = datetime.fromisoformat(new_entry["next_occurrence"].replace('Z', '+00:00'))
                self.schedule_recurring_task({
                    "sid": new_sid,
                    "frequency": frequency,
                    "next_occurrence": new_entry["next_occurrence"]
                })
                
                # Also schedule deadline monitoring for the new entry
                self.schedule_deadline_monitoring(new_entry)
            else:
                logger.error(f"Failed to create new recurring entry for task {current_entry['tid']}")
                
        except Exception as e:
            logger.error(f"Error processing recurring task {sid}: {str(e)}")

    def cancel_recurring_task(self, sid: str):
        """
        Cancel a scheduled recurring task
        """
        try:
            job_id = f"recurring_{sid}"
            
            # Check if job exists before trying to remove it
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                logger.info(f"Cancelled recurring task {sid}")
            else:
                logger.info(f"Recurring task {sid} was not scheduled (no job found)")
            
            return True
        except Exception as e:
            logger.error(f"Error cancelling recurring task {sid}: {str(e)}")
            return False

    def cancel_deadline_monitoring(self, sid: str):
        """
        Cancel scheduled deadline monitoring jobs (both approaching and overdue)
        """
        try:
            # Cancel approaching notification job
            approaching_job_id = f"deadline_approaching_{sid}"
            if self.scheduler.get_job(approaching_job_id):
                self.scheduler.remove_job(approaching_job_id)
                logger.info(f"Cancelled deadline approaching notification for {sid}")
            else:
                logger.info(f"Deadline approaching notification for {sid} was not scheduled (no job found)")
            
            # Cancel overdue notification job
            overdue_job_id = f"deadline_{sid}"
            if self.scheduler.get_job(overdue_job_id):
                self.scheduler.remove_job(overdue_job_id)
                logger.info(f"Cancelled deadline overdue notification for {sid}")
            else:
                logger.info(f"Deadline overdue notification for {sid} was not scheduled (no job found)")
            
            return True
        except Exception as e:
            logger.error(f"Error cancelling deadline monitoring for {sid}: {str(e)}")
            return False

    def cancel_all_task_jobs(self, sid: str):
        """
        Cancel both recurring and deadline monitoring jobs for a task
        """
        try:
            recurring_cancelled = self.cancel_recurring_task(sid)
            deadline_cancelled = self.cancel_deadline_monitoring(sid)
            
            return recurring_cancelled and deadline_cancelled
        except Exception as e:
            logger.error(f"Error cancelling all jobs for {sid}: {str(e)}")
            return False

    def get_scheduled_jobs(self):
        """
        Get all currently scheduled jobs
        """
        jobs = self.scheduler.get_jobs()
        return [{"id": job.id, "next_run_time": job.next_run_time} for job in jobs]

    def shutdown(self):
        """
        Shutdown the scheduler
        """
        self.scheduler.shutdown()
        logger.info("RecurringTaskProcessor shutdown")

# Global instance
recurring_processor = RecurringTaskProcessor()
