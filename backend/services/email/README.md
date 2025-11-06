# Email Service 📧

A Python microservice for sending emails via SMTP and managing email notifications.  
The service runs as a Kafka consumer, listening for notification events, and also sends daily email summaries to staff members.

---

## 🚀 Features

-   **Real-time Email Notifications**: Receives notification events from Kafka and sends emails for:

    -   Task assignments
    -   Deadline approaching (3 days before)
    -   Deadline overdue
    -   Task updates
    -   Task deletions
    -   Project collaborator additions

-   **Daily Email Summary**: Automatically sends daily task summaries to all staff members at 8:15 AM UTC+8 (Singapore time) with:
    -   Tasks due today
    -   Tasks due tomorrow
    -   Tasks overdue
    -   Overall status (Ongoing Tasks)

---

## 🛠️ How to Run

### Using Docker

cd into the email folder then run the docker code

```bash
docker build -t email .
docker run --env-file .env email
```

The service will:

1. Start as a Kafka consumer listening for notification events
2. Automatically schedule daily email summaries at 8:15 AM UTC+8

### Environment Variables

Required environment variables in `.env`:

```env
# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=kafka:9093

# Service URLs (for daily summaries)
TASK_SERVICE_URL=http://tasks:5500
USERS_SERVICE_URL=http://user:5100
SCHEDULE_SERVICE_URL=http://schedule:5300
MANAGE_TASK_SERVICE_URL=http://manage-task:4100
PROJECTS_SERVICE_URL=http://project:5200
INTERNAL_API_KEY=your-internal-api-key
```

---

## 📧 Daily Email Summary

### Automatic Scheduling

Daily email summaries are automatically sent to all staff members (role: `staff`, `manager`, or `hr`) at **8:15 AM UTC+8** every day.

### Manual Trigger (for testing)

You can manually trigger the daily summary by running:

```bash
python main.py --send-daily-summary
```

Or programmatically:

```python
from main import EmailService
from daily_email_summary import DailyEmailSummaryService

email_service = EmailService()
daily_summary_service = DailyEmailSummaryService(email_service)
daily_summary_service.send_daily_summaries()
```

### Email Content

Each daily summary includes:

-   **Overdue Tasks**: Tasks with deadlines that have passed
-   **Tasks Due Today**: Tasks with deadlines today
-   **Tasks Due Tomorrow**: Tasks with deadlines tomorrow
-   **Ongoing Tasks**: All tasks with status "ongoing"

Each task entry shows:

-   Task name
-   Project name
-   Priority level
-   Deadline (formatted in UTC+8)

---

## 🔧 Configuration

### Changing the Daily Summary Time

To change the time when daily summaries are sent, edit `main.py`:

```python
# In setup_daily_email_scheduler function
scheduler.add_job(
    func=daily_summary_service.send_daily_summaries,
    trigger=CronTrigger(hour=8, minute=15, timezone=UTC_PLUS_8),  # Change hour and minute here
    id='daily_email_summary',
    name='Daily Email Summary at 8:15 AM',
    replace_existing=True
)
```

### Service URLs

The daily email summary service needs to connect to other microservices. Make sure these URLs are correctly configured in your `.env` file or environment variables.

---

## 📝 How it Works

1. **Kafka Consumer**: Listens to the `notification-events` topic for real-time notifications
2. **Daily Scheduler**: Uses APScheduler to run daily email summaries at the configured time
3. **Task Querying**: Fetches tasks for each staff member from the composite `manage-task` service
4. **Task Categorization**: Categorizes tasks by deadline (overdue, due today, due tomorrow) and status (ongoing)
5. **Email Generation**: Formats and sends personalized email summaries to each staff member
