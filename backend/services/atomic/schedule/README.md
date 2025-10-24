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

### Get All Recurring Tasks

GET http://localhost:5300/recurring/all

Sample Output:

```json
{
    "message": "Retrieved 2 recurring tasks",
    "tasks": [
        {
            "tid": "1991067d-18d4-48c4-987b-7c06743725b4",
            "start": "2025-09-25T15:42:21+00:00",
            "deadline": "2025-09-26T15:42:21+00:00",
            "is_recurring": false,
            "status": "ongoing",
            "created_at": "2025-09-25T15:42:21+00:00",
            "next_occurrence": null,
            "sid": "6c2c6617-971d-4c30-a0ec-263c386bc937"
        },
        {
            "tid": "b1692687-4e49-41b1-bb04-3f5c18d6faf7",
            "start": "2025-09-25T15:42:21+00:00",
            "deadline": "2025-09-26T15:42:21+00:00",
            "is_recurring": false,
            "status": "ongoing",
            "created_at": "2025-09-25T15:42:21+00:00",
            "next_occurrence": null,
            "sid": "6c2c6617-971d-4c30-a0ec-263c386bc938"
        }
    ]
}
```


