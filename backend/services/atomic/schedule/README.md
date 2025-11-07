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

## Access API docs at: http://localhost:5300/docs#

### Health Check

GET http://localhost:5300

Output:

```bash
"message": "Schedule Service is running 🚀😌"
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

### Get Schedule w Task ID

GET http://localhost:5300/tid/{tid}

> http://localhost:5300/tid/619269be-0d73-4073-a02b-c32bb3216c37

Sample Output:

```json
{
  "message": "Task 619269be-0d73-4073-a02b-c32bb3216c37 Schedule Retrieved Successfully",
  "data": [
    {
      "tid": "619269be-0d73-4073-a02b-c32bb3216c37",
      "deadline": "2025-11-24T16:00:00+00:00",
      "status": "in_progress",
      "created_at": "2025-11-06T21:07:18.340973+00:00",
      "is_recurring": false,
      "next_occurrence": null,
      "start": "2025-11-05T16:00:00+00:00",
      "sid": "0f89b3b9-00f4-4a3a-8214-664191600375",
      "frequency": null
    }
  ]
}
```


### Update schedule by task id

PUT http://localhost:5300/tid/{tid}

> http://localhost:5300/tid/619269be-0d73-4073-a02b-c32bb3216c37

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
  "message": "Task 619269be-0d73-4073-a02b-c32bb3216c37 Schedule Updated Successfully",
  "data": {
    "tid": "619269be-0d73-4073-a02b-c32bb3216c37",
    "deadline": "2026-01-26T15:42:21+00:00",
    "status": "overdue",
    "created_at": "2025-11-06T21:07:18.340973+00:00",
    "is_recurring": true,
    "next_occurrence": "2026-09-26T15:42:21+00:00",
    "start": "2025-11-05T16:00:00+00:00",
    "sid": "0f89b3b9-00f4-4a3a-8214-664191600375",
    "frequency": null
  }
}
```

### Get Schedule w Task ID Latest

GET http://localhost:5300/tid/{task_id}/latest

> http://localhost:5300/tid/619269be-0d73-4073-a02b-c32bb3216c37/latest

Sample Output:

```json
{
  "message": "Task 619269be-0d73-4073-a02b-c32bb3216c37 Schedule Retrieved Successfully",
  "data": {
    "tid": "619269be-0d73-4073-a02b-c32bb3216c37",
    "deadline": "2026-01-26T15:42:21+00:00",
    "status": "overdue",
    "created_at": "2025-11-06T21:07:18.340973+00:00",
    "is_recurring": true,
    "next_occurrence": "2026-09-26T15:42:21+00:00",
    "start": "2025-11-05T16:00:00+00:00",
    "sid": "0f89b3b9-00f4-4a3a-8214-664191600375",
    "frequency": null
  }
}
```

### Get Schedule w Schedule ID

GET http://localhost:5300/sid/{sid}

> http://localhost:5300/sid/f6164f22-dc33-40df-80bc-5d7034a4dd36

Sample Output:

```json
{
  "message": "Task Schedule f6164f22-dc33-40df-80bc-5d7034a4dd36 Retrieved Successfully",
  "data": {
    "tid": "082865a8-44c1-4f5e-8e9f-b74282eae6be",
    "deadline": "2025-11-01T09:34:48+00:00",
    "status": "overdue",
    "created_at": "2025-10-24T09:34:56.465899+00:00",
    "is_recurring": null,
    "next_occurrence": null,
    "start": "2025-10-24T09:34:44+00:00",
    "sid": "f6164f22-dc33-40df-80bc-5d7034a4dd36",
    "frequency": null
  }
}
```


### Update Existing Schedule

PUT http://localhost:5300/{sid}

> http://localhost:5300/f6164f22-dc33-40df-80bc-5d7034a4dd36

Sample Input:

```json
{
    "status": "overduehehe",
    "deadline": "2026-01-26T15:42:21Z",
    "next_occurrence": "2026-09-26T15:42:21Z",
    "is_recurring": true
}
```

Sample Output:

```json
{
  "message": "Task Schedule f6164f22-dc33-40df-80bc-5d7034a4dd36 Updated Successfully",
  "data": {
    "tid": "082865a8-44c1-4f5e-8e9f-b74282eae6be",
    "deadline": "2026-01-26T15:42:21+00:00",
    "status": "overduehehe",
    "created_at": "2025-10-24T09:34:56.465899+00:00",
    "is_recurring": true,
    "next_occurrence": "2026-09-26T15:42:21+00:00",
    "start": "2025-10-24T09:34:44+00:00",
    "sid": "f6164f22-dc33-40df-80bc-5d7034a4dd36",
    "frequency": null
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

DELETE http://localhost:5300/{sid}

> http://localhost:5300/f6164f22-dc33-40df-80bc-5d7034a4dd36

Sample Output:

```json
{
  "message": "Task Schedule f6164f22-dc33-40df-80bc-5d7034a4dd36 deleted successfully"
}
```

### Get All Recurring Tasks

GET http://localhost:5300/recurring/all

Sample Output:

```json
{
  "tasks": [
    {
      "tid": "ea5cb2c2-336c-4d33-927d-bdd1ef2f5406",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-05T18:38:14.392218+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "6d5d3cf6-4e78-4e12-bde7-8c03d7af59b6",
      "frequency": "weekly"
    },
    {
      "tid": "b318dbe4-92fb-42f1-a307-80d497aa1a24",
      "deadline": "2025-11-03T16:00:00+00:00",
      "status": "overdue",
      "created_at": "2025-11-04T09:53:21.619465+00:00",
      "is_recurring": true,
      "next_occurrence": "2025-11-07T16:00:00+00:00",
      "start": "2025-10-31T16:00:00+00:00",
      "sid": "d9995fd2-f01b-407f-8957-ac3c0c83b732",
      "frequency": "weekly"
    },
    {
      "tid": "552b91c4-e799-40ea-9549-3d3d735d5482",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-10-25T09:00:28.979163+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "9c7e2ccb-506b-48cd-8cf5-481da400658d",
      "frequency": "weekly"
    },
    {
      "tid": "a6f7d5f7-6a91-48d3-96af-8dc7a7ddf3a0",
      "deadline": "2025-12-31T23:59:59+00:00",
      "status": "ongoing",
      "created_at": "2025-10-23T17:42:59.402902+00:00",
      "is_recurring": true,
      "next_occurrence": "2025-12-31T23:59:59+00:00",
      "start": "2024-10-20T09:00:00+00:00",
      "sid": "4397ede5-b461-4c06-a5c6-7ed16ca92388",
      "frequency": "weekly"
    },
    {
      "tid": "fd0e7ac3-c82e-49fa-af79-44e15c114b2f",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "ongoing",
      "created_at": "2025-10-23T19:15:13.344227+00:00",
      "is_recurring": true,
      "next_occurrence": "2025-10-28T16:00:00+00:00",
      "start": "2025-10-21T16:00:00+00:00",
      "sid": "28418b7d-0d33-4ef6-b7c2-9932c692ceb1",
      "frequency": "weekly"
    },
    {
      "tid": "10166f86-cda5-44e5-994a-3287b326ed45",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T07:50:40.725467+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "fb81953d-19d6-46ad-bd73-d4130725e98d",
      "frequency": "weekly"
    },
    {
      "tid": "ba9f12ab-57a4-4492-8d10-ad8881d300b8",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T08:58:38.270761+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "717d942c-a2d9-4581-8ba2-89d64ca47518",
      "frequency": "weekly"
    },
    {
      "tid": "9ccc8b77-e159-40cd-8b9b-c29adfbae6f9",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T08:59:38.936561+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "0debd677-7978-42e8-b482-8f5b55f1efd4",
      "frequency": "weekly"
    },
    {
      "tid": "3d5ccfc7-1511-43ea-94c1-2725935e2c70",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:02:35.262178+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "ee22ae23-58ec-4b11-bd91-b538d21cc4a9",
      "frequency": "weekly"
    },
    {
      "tid": "9a2b9205-119c-4f6b-81a4-8698c5afe3a6",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:06:52.821875+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "015d34ee-c5bd-41c9-91e5-d4929e5bed8c",
      "frequency": "weekly"
    },
    {
      "tid": "c6d6288d-4db6-45cb-81f2-917e6d81fd13",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:14:03.047863+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "3d4d8a07-113e-431b-88e8-d35b639d312d",
      "frequency": "weekly"
    },
    {
      "tid": "c34d04a1-2ce1-4602-89f8-aa4bf4f248c8",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:15:08.969985+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "93a63482-ad45-4e6f-8231-81902114cdfe",
      "frequency": "weekly"
    },
    {
      "tid": "b681a7b9-fe29-4e0c-8d35-a4cc79fd4596",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:25:26.376526+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "a219c1c3-53f3-4a27-91d4-018ec286e32b",
      "frequency": "weekly"
    },
    {
      "tid": "cbada179-6a7e-48a5-b1bf-4aa486535d64",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:36:44.879352+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "9cd06977-8914-4097-8632-dcdedd477163",
      "frequency": "weekly"
    },
    {
      "tid": "31b3d193-1485-4867-8e47-cf1c72fe3067",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:42:27.959033+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "71a46c15-0df9-474f-8cf2-d5fd2dea809f",
      "frequency": "weekly"
    },
    {
      "tid": "12aedcf6-4705-43d8-968e-dcbf2bd73de0",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:46:01.377723+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "21236bee-a95b-4d83-a854-bc6bf8e3c931",
      "frequency": "weekly"
    },
    {
      "tid": "b89f3c56-840a-43c6-b4ea-9473fa3c1220",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:48:03.873723+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "39c2b3d2-8638-485a-8a2d-4f22102b144d",
      "frequency": "weekly"
    },
    {
      "tid": "c3299c20-ef97-45d2-9a2d-774d2990e78a",
      "deadline": "2026-12-31T23:59:59+00:00",
      "status": "done",
      "created_at": "2025-11-04T09:51:25.943276+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-12-31T23:59:59+00:00",
      "start": "2025-10-20T09:00:00+00:00",
      "sid": "52cf0bb3-e4af-40e7-b9d7-cb18a7474004",
      "frequency": "weekly"
    },
    {
      "tid": "619269be-0d73-4073-a02b-c32bb3216c37",
      "deadline": "2026-01-26T15:42:21+00:00",
      "status": "overdue",
      "created_at": "2025-11-06T21:07:18.340973+00:00",
      "is_recurring": true,
      "next_occurrence": "2026-09-26T15:42:21+00:00",
      "start": "2025-11-05T16:00:00+00:00",
      "sid": "0f89b3b9-00f4-4a3a-8214-664191600375",
      "frequency": null
    }
  ]
}
```


