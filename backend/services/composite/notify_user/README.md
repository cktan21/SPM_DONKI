## Instructions

> Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 4500
```

To deactivate server:

```bash
deactivate
```

> Docker Development

```bash
docker build -t my-fastapi-app .
docker run -p 4500:4500 --name my-fastapi-container my-fastapi-app
```

## EndPoints

### Health Check

GET http://localhost:4500

Output:

```bash
"message": "Notify User Service is running 🚀😌"
```

### Get All Recurring Tasks

GET http://localhost:4500/task/recurring

Sample Output:
```json
{
    "message": "Retrieved 3 recurring tasks",
    "tasks": [
        {
            "tid": "a6f7d5f7-6a91-48d3-96af-8dc7a7ddf3a0",
            "deadline": "2025-12-31T23:59:59+00:00",
            "status": "done",
            "created_at": "2025-10-23T17:42:59.402902+00:00",
            "is_recurring": true,
            "next_occurrence": "2025-12-31T23:59:59+00:00",
            "start": "2024-10-20T09:00:00+00:00",
            "sid": "4397ede5-b461-4c06-a5c6-7ed16ca92388",
            "frequency": "weekly"
        },
        {
            "tid": "ac4a5335-12b4-4e04-8c4e-394059299213",
            "deadline": "2025-12-31T23:59:59+00:00",
            "status": "done",
            "created_at": "2025-10-23T17:56:02.663256+00:00",
            "is_recurring": true,
            "next_occurrence": "2025-12-31T23:59:59+00:00",
            "start": "2024-10-20T09:00:00+00:00",
            "sid": "ac28a0ef-dd72-43ed-8afc-a1dc2b782231",
            "frequency": "weekly"
        },
        {
            "tid": "fd0e7ac3-c82e-49fa-af79-44e15c114b2f",
            "deadline": "2026-12-31T23:59:59+00:00",
            "status": "in_progress",
            "created_at": "2025-10-23T19:15:13.344227+00:00",
            "is_recurring": true,
            "next_occurrence": "2025-10-28T16:00:00+00:00",
            "start": "2025-10-21T16:00:00+00:00",
            "sid": "28418b7d-0d33-4ef6-b7c2-9932c692ceb1",
            "frequency": "weekly"
        }
    ]
}
```

### Get Scheduled Jobs (Jobs Currently Scheduled in the Recurring Processor)

GET http://localhost:4500/task/scheduled

Sample Output:

```json
{
    "message": "Retrieved 3 scheduled jobs",
    "jobs": [
        {
            "id": "recurring_28418b7d-0d33-4ef6-b7c2-9932c692ceb1",
            "next_run_time": "2025-10-28T16:00:00+00:00"
        },
        {
            "id": "recurring_4397ede5-b461-4c06-a5c6-7ed16ca92388",
            "next_run_time": "2025-12-31T23:59:59+00:00"
        },
        {
            "id": "recurring_ac28a0ef-dd72-43ed-8afc-a1dc2b782231",
            "next_run_time": "2025-12-31T23:59:59+00:00"
        }
    ]
}
```

## Recurring Task Functionality

The schedule service now supports automatic recurring task creation using APScheduler. When a task is marked as recurring with a frequency, the system will:

1. **Automatically create new schedule entries** when the `next_occurrence` time is reached
2. **Maintain the same time gap** between start and deadline as the original task
3. **Calculate the next occurrence** based on the frequency:
    - **Weekly**: Adds 1 week to the start time
    - **Monthly**: Adds 1 month to the start time
    - **Yearly**: Adds 1 year to the start time
    - **Immediate**: Creates the next entry 1 minute after the deadline

### How It Works

1. When you create a recurring task, the system schedules a background job
2. At the `next_occurrence` time, the system:

    - Creates a new schedule entry with the same task ID
    - Calculates new start/deadline times maintaining the original gap
    - Sets up the next occurrence based on frequency
    - Schedules the next recurring job

3. The process continues automatically until the task is deleted or marked as non-recurring

### Example Recurring Task Creation

```json
{
    "tid": "1e5233e4-be0f-4f94-9c59-c6a72debe0aa",
    "start": "2025-10-18T06:43:45Z",
    "deadline": "2025-10-25T06:43:45Z",
    "is_recurring": true,
    "next_occurrence": "2025-11-18T06:43:45Z",
    "frequency": "Monthly"
}
```

This will create a new entry every month starting from November 18th, 2025, with the same 7-day gap between start and deadline.
