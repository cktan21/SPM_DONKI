from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from dateutil.relativedelta import relativedelta
from schedule_client import ScheduleClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecurringTaskProcessor:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.schedule_client = ScheduleClient()
        self.scheduler.start()
        logger.info("RecurringTaskProcessor initialized and scheduler started")

    def calculate_next_occurrence(self, frequency: str, current_start: datetime, current_deadline: datetime) -> datetime:
        """
        Calculate the next occurrence based on frequency and the gap between start and deadline
        """
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
                self.schedule_recurring_task(new_sid, frequency, new_next_occurrence)
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
