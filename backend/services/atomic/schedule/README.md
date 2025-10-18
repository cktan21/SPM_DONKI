## Instructions

> Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5300
```

To deactivate server:

```bash
deactivate
```

> Docker Development

```bash
docker build -t my-fastapi-app .
docker run -p 5300:5300 --name my-fastapi-container my-fastapi-app
```

## EndPoints

### Health Check

GET http://localhost:5300

Output:

```bash
"message": "Schedule Service is running 🚀😌"
```

### Get Schedule w Task ID

GET http://localhost:5300/{task_id}

> http://localhost:5300/tid/1e5233e4-be0f-4f94-9c59-c6a72debe0aa

Sample Output:

```json
{
    "message": "Task 1e5233e4-be0f-4f94-9c59-c6a72debe0aa Schedule Retrieved Successfully",
    "data": [
        {
            "tid": "1e5233e4-be0f-4f94-9c59-c6a72debe0aa",
            "deadline": "2026-01-26T15:42:21+00:00",
            "status": "overdue",
            "created_at": "2025-10-18T07:35:10.706153+00:00",
            "is_recurring": true,
            "next_occurrence": "2026-09-26T15:42:21+00:00",
            "start": "2025-11-26T15:42:21+00:00",
            "sid": "053a4e96-cefd-4a8e-9941-5b621ff8ca52"
        },
        {
            "tid": "1e5233e4-be0f-4f94-9c59-c6a72debe0aa",
            "deadline": "2025-03-20T08:06:06+00:00",
            "status": "ongoing",
            "created_at": "2025-10-18T08:34:34.969657+00:00",
            "is_recurring": true,
            "next_occurrence": "2025-10-18T08:34:20+00:00",
            "start": "2025-01-08T08:33:28+00:00",
            "sid": "9f7c031a-41b7-4fbd-813b-b3b4e66bb11a"
        }
    ]
}
```

### Get Schedule w Task ID Latest

GET http://localhost:5300/tid/{task_id}/latest

> http://localhost:5300/tid/1e5233e4-be0f-4f94-9c59-c6a72debe0aa/latest

Sample Output:

```json
{
    "message": "Task 1e5233e4-be0f-4f94-9c59-c6a72debe0aa Schedule Retrieved Successfully",
    "data": {
        "tid": "1e5233e4-be0f-4f94-9c59-c6a72debe0aa",
        "deadline": "2025-03-20T08:06:06+00:00",
        "status": "ongoing",
        "created_at": "2025-10-18T08:34:34.969657+00:00",
        "is_recurring": true,
        "next_occurrence": "2025-10-18T08:34:20+00:00",
        "start": "2025-01-08T08:33:28+00:00",
        "sid": "9f7c031a-41b7-4fbd-813b-b3b4e66bb11a"
    }
}
```

### Get Schedule w Schedule ID

GET http://localhost:5300/sid/{schedule_id}

> http://localhost:5300/sid/053a4e96-cefd-4a8e-9941-5b621ff8ca52

Sample Output:

```json
{
    "message": "Task Schedule 053a4e96-cefd-4a8e-9941-5b621ff8ca52 Retrieved Successfully",
    "data": {
        "tid": "1e5233e4-be0f-4f94-9c59-c6a72debe0aa",
        "deadline": "2026-01-26T15:42:21+00:00",
        "status": "overdue",
        "created_at": "2025-10-18T07:35:10.706153+00:00",
        "is_recurring": true,
        "next_occurrence": "2026-09-26T15:42:21+00:00",
        "start": "2025-11-26T15:42:21+00:00",
        "sid": "053a4e96-cefd-4a8e-9941-5b621ff8ca52"
    }
}
```

### Insert New Schedule

POST http://localhost:5300

> http://localhost:5300

Sample Input:

```json
{
    "tid": "1e5233e4-be0f-4f94-9c59-c6a72debe0aa",
    "deadline": "2025-12-10T15:42:21Z",
    "start": "2025-11-26T15:42:21Z",
    "is_recurring": true,
    "next_occurrence": "2026-09-26T15:42:21Z"
}
```

Sample Output:

```json
{
    "message": "Task 1e5233e4-be0f-4f94-9c59-c6a72debe0aa Schedule Inserted Successfully",
    "data": {
        "tid": "1e5233e4-be0f-4f94-9c59-c6a72debe0aa",
        "deadline": "2025-12-10T15:42:21+00:00",
        "status": "ongoing",
        "created_at": "2025-10-18T07:35:10.706153+00:00",
        "is_recurring": true,
        "next_occurrence": "2026-09-26T15:42:21+00:00",
        "start": "2025-11-26T15:42:21+00:00",
        "sid": "053a4e96-cefd-4a8e-9941-5b621ff8ca52"
    }
}
```

### Note:

-   New Schedule status is always assumed to be `ongoing` hence not requiring a field
-   if not `start` is provided it will be set to the current time
-   ensure that `start` < `deadline` < `next_occurrence`
    -   eg: `{"start": "2025-10-11T11:58:20+08:00", "deadline": "2025-10-11T11:58:20+08:00", "next_occurrence": "2025-10-11T11:58:20+08:00"}` is valid
    -   eg: `{"start": "2025-10-11T11:58:20+08:00", "deadline": "2025-10-11T11:58:20+08:00", "next_occurrence": "2025-10-10T11:58:20+08:00"}` is invalid
-   **One** Task can only have _MULTIPLE entries_ in schedule
    -   Each entry is a different occurrence of the task
-   `is_recurring` is a boolean field, default is `False`
-   `next_occurrence` is a datetime field, default is `None`
    -   if `is_recurring` is `True`, `next_occurrence` is the next occurrence of the task
    -   if `is_recurring` is `False`, `next_occurrence` is `None`
-   `frequency` is a string field for recurring tasks, supported values:
    -   `"Weekly"` - Creates new entries weekly
    -   `"Monthly"` - Creates new entries monthly
    -   `"Yearly"` - Creates new entries yearly
    -   `"Immediate"` - Creates new entries immediately after deadline

### Update Existing Schedule

PUT http://localhost:5300/{schedule_id}

> http://localhost:5300/053a4e96-cefd-4a8e-9941-5b621ff8ca52

Sample Input:

```json
{
    "status": "overdue",
    "deadline": "2026-01-26T15:42:21Z",
    "next_occurrence": "2026-09-26T15:42:21Z",
    "is_recurring": true
}
```

Sample Output:

```json
{
    "message": "Task Schedule 053a4e96-cefd-4a8e-9941-5b621ff8ca52 Updated Successfully",
    "data": {
        "tid": "1e5233e4-be0f-4f94-9c59-c6a72debe0aa",
        "deadline": "2026-01-26T15:42:21+00:00",
        "status": "overdue",
        "created_at": "2025-10-18T07:35:10.706153+00:00",
        "is_recurring": true,
        "next_occurrence": "2026-09-26T15:42:21+00:00",
        "start": "2025-11-26T15:42:21+00:00",
        "sid": "053a4e96-cefd-4a8e-9941-5b621ff8ca52"
    }
}
```

### Note:

-   `schedule_id` has to exist in the db otherwise it will return an error
-   ensure that `start` < `deadline` < `next_occurrence`
-   `status`, `deadline` and `start` are not mandatory fields, you can change one without changing the other
    -   eg: `{"status": "overdue"}` and `{"deadline": "2025-10-11T11:58:20+08:00"}` and `{"start": "2025-10-11T11:58:20+08:00"}` both valid inputs
-   if you want to update the `is_recurring` field to `true`, you need to provide the `next_occurrence` field
    -   eg: `{"is_recurring": true, "next_occurrence": "2026-09-26T15:42:21Z"}`

### Delete Schedule w Schedule ID

DELETE http://localhost:5300/{schedule_id}

> http://localhost:5300/053a4e96-cefd-4a8e-9941-5b621ff8ca52

Sample Output:

```json
{
    "message": "Task Schedule 3ac06674-a63f-4dea-8f2a-2f3e645d58b4 deleted successfully"
}
```

### Get Scheduled Recurring Tasks

GET http://localhost:5300/recurring/scheduled

Sample Output:

```json
{
    "message": "Found 3 scheduled recurring tasks",
    "jobs": [
        {
            "id": "recurring_053a4e96-cefd-4a8e-9941-5b621ff8ca52",
            "next_run_time": "2025-10-18T08:34:20+00:00"
        },
        {
            "id": "recurring_9f7c031a-41b7-4fbd-813b-b3b4e66bb11a",
            "next_run_time": "2025-11-18T08:34:20+00:00"
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
