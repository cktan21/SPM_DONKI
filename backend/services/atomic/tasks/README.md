## Instructions
> Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5500
```

To deactivate server:
```bash
deactivate
```
> Docker Development
```bash
docker build -t my-fastapi-app .
docker run -p 5500:5500 --name my-fastapi-container my-fastapi-app
```

## EndPoints

## Access API docs at: http://localhost:5500/docs#

### Health Check

GET http://localhost:5500

Output:
```bash
"message": "Task Service is running 🚀😱"
```

### Get All Tasks

GET http://localhost:5500/tasks

Retrieve all tasks in the system.

Sample Output:
```json
{
    "message": "2 task(s) retrieved",
    "tasks": [
        {
            "id": "1991067d-18d4-48c4-987b-7c06743725b4",
            "name": "get coffee",
            "created_by_uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
            "updated_timestamp": "2025-09-14T14:26:42.564234+00:00",
            "parentTaskId": "b1692687-4e49-41b1-bb04-3f5c18d6faf7",
            "collaborators": null,
            "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "desc": "black coffee w latte",
            "notes": null
        },
        {
            "id": "b1692687-4e49-41b1-bb04-3f5c18d6faf7",
            "name": "Complete Project Setup2",
            "created_by_uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
            "updated_timestamp": "2025-09-16T16:40:34.659965+00:00",
            "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
            "collaborators": [
                "3e3b2d6c-6d6b-4dc0-9b76-0b6b3fe9c001",
                "f7f5cf6e-1c3a-4d3a-8d50-5a2f60d9a002"
            ],
            "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "desc": "Set up the initial project structure and dependencies",
            "notes": "Remember to update the README file"
        }
    ]
}

### Get task by task ID

GET http://localhost:5500/tid/{task_id}

> http://localhost:5500/tid/eaa5765c-7c39-435b-933c-667c0e27f872

Sample Output:
```json
{
  "message": "Task retrieved successfully",
  "task": {
    "id": "eaa5765c-7c39-435b-933c-667c0e27f872",
    "name": "very beaucratic very demure wowo",
    "created_by_uid": "655a9260-f871-480f-abea-ded735b2170a",
    "updated_timestamp": "2025-11-06T15:14:26.769642+00:00",
    "parentTaskId": null,
    "collaborators": [
      "6933d965-e4c4-4b49-bc99-08236b1d9458"
    ],
    "pid": "352486e8-a727-470c-add4-10fe26f1fbce",
    "desc": null,
    "notes": null,
    "priorityLevel": 3,
    "label": "bug",
    "messages": [],
    "time_entries": [],
    "subtasks": []
  }
}
```

### Get task by project ID

GET http://localhost:5500/pid/{project_id}

> http://localhost:5500/pid/f434f31d-3c12-4867-889c-794edf0c6199

Sample Output:
```json
{
  "message": "5 task(s) retrieved",
  "tasks": [
    {
      "id": "799f0bd8-ab9b-430c-921c-18c3036a46e5",
      "name": "Test add",
      "created_by_uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
      "updated_timestamp": "2025-10-25T06:50:00.479541+00:00",
      "parentTaskId": null,
      "collaborators": [
        "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
      ],
      "pid": "f434f31d-3c12-4867-889c-794edf0c6199",
      "desc": "Test add",
      "notes": "tEST",
      "priorityLevel": 9,
      "label": "feature",
      "messages": [],
      "time_entries": []
    },
    {
      "id": "082865a8-44c1-4f5e-8e9f-b74282eae6be",
      "name": "Nonna",
      "created_by_uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
      "updated_timestamp": "2025-10-24T08:19:00.044947+00:00",
      "parentTaskId": null,
      "collaborators": null,
      "pid": "f434f31d-3c12-4867-889c-794edf0c6199",
      "desc": null,
      "notes": null,
      "priorityLevel": 5,
      "label": "bug",
      "messages": [],
      "time_entries": []
    },
    {
      "id": "e86267cd-d90d-4109-aa0d-b8dac632d10d",
      "name": "test non collab or creator of teststaff",
      "created_by_uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "updated_timestamp": "2025-10-24T08:23:41.169878+00:00",
      "parentTaskId": null,
      "collaborators": null,
      "pid": "f434f31d-3c12-4867-889c-794edf0c6199",
      "desc": null,
      "notes": null,
      "priorityLevel": 5,
      "label": "bug",
      "messages": [],
      "time_entries": []
    },
    {
      "id": "91b99851-e1e5-4d99-85f8-e37b0ecbfae7",
      "name": "Test add 2",
      "created_by_uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
      "updated_timestamp": "2025-10-25T06:56:07.577605+00:00",
      "parentTaskId": null,
      "collaborators": [
        "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
      ],
      "pid": "f434f31d-3c12-4867-889c-794edf0c6199",
      "desc": "test",
      "notes": "test",
      "priorityLevel": 1,
      "label": "maintenance",
      "messages": [],
      "time_entries": []
    },
    {
      "id": "fd0e7ac3-c82e-49fa-af79-44e15c114b2f",
      "name": "Update task from composite service",
      "created_by_uid": "655a9260-f871-480f-abea-ded735b2170a",
      "updated_timestamp": "2025-10-24T02:24:32.731541+00:00",
      "parentTaskId": "082865a8-44c1-4f5e-8e9f-b74282eae6be",
      "collaborators": [
        "655a9260-f871-480f-abea-ded735b2170a",
        "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "fb892a63-2401-46fc-b660-bf3fe1196d4e"
      ],
      "pid": "f434f31d-3c12-4867-889c-794edf0c6199",
      "desc": "Set up the initial project structure and dependencies",
      "notes": "Remember to update the README file",
      "priorityLevel": 2,
      "label": "SetupUpdated",
      "messages": [],
      "time_entries": []
    }
  ]
}
```

### Get task by parent Task ID

GET http://localhost:5500/ptid/{parent_task_id}

> http://localhost:5500/ptid/33949f99-20d0-423d-9b26-f09292b2e40d

Sample Output:

```json
{
    "message": "2 child task(s) retrieved",
    "tasks": [
        {
            "id": "d695f875-a0c9-42b3-baf9-a367a437367d",
            "name": "New Task Title",
            "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
            "updated_timestamp": "2025-10-05T22:26:16.650616+00:00",
            "parentTaskId": "33949f99-20d0-423d-9b26-f09292b2e40d",
            "collaborators": [
                "fb892a63-2401-46fc-b660-bf3fe1196d4e",
                "655a9260-f871-480f-abea-ded735b2170a"
            ],
            "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "desc": "Optional description",
            "notes": "Optional notes",
            "priorityLevel": 5,
            "priorityLabel": "Medium"
        },
        {
            "id": "be238e36-2506-432a-a267-e2a1308ff22b",
            "name": "New Task Title2",
            "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
            "updated_timestamp": "2025-10-06T08:39:43.761577+00:00",
            "parentTaskId": "33949f99-20d0-423d-9b26-f09292b2e40d",
            "collaborators": [
                "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
                "fb892a63-2401-46fc-b660-bf3fe1196d4e"
            ],
            "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "desc": "Optional description",
            "notes": "Optional notes",
            "priorityLevel": 5,
            "priorityLabel": "Medium"
        }
    ]
}
```

### Create Task

POST http://localhost:5500/createTask

> http://localhost:5500/createTask

Create a new task (include pid if task belongs to a project, parentTaskId if it’s a subtask)

Sample Request Body:
```json
{
    "name": "New Task Title 7Nov",
    "created_by_uid": "17a40371-66fe-411a-963b-a977cc7cb475",
    "pid": "352486e8-a727-470c-add4-10fe26f1fbce",
    "collaborators": [
        "17a40371-66fe-411a-963b-a977cc7cb475",
        "655a9260-f871-480f-abea-ded735b2170a"
    ],
    "desc": "Optional description",
    "notes": "Optional notes"
}
```

Sample Output:
```json
{
  "message": "Task created successfully",
  "task": {
    "id": "5c2e225d-33af-4663-b14a-41716bfc6626",
    "name": "New Task Title 7Nov",
    "created_by_uid": "17a40371-66fe-411a-963b-a977cc7cb475",
    "updated_timestamp": "2025-11-07T12:15:33.248458+00:00",
    "parentTaskId": null,
    "collaborators": [
      "17a40371-66fe-411a-963b-a977cc7cb475",
      "655a9260-f871-480f-abea-ded735b2170a"
    ],
    "pid": "352486e8-a727-470c-add4-10fe26f1fbce",
    "desc": "Optional description",
    "notes": "Optional notes",
    "priorityLevel": 5,
    "label": "bug",
    "messages": [],
    "time_entries": []
  }
}
```

### Update Task

PUT http://localhost:5500/{task_id}

> http://localhost:5500/5c2e225d-33af-4663-b14a-41716bfc6626

Update task details by task id

Sample Request Body:
```json
{
  "name": "Complete Project Setup 7Nov"
}
```

Sample Output:
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": "5c2e225d-33af-4663-b14a-41716bfc6626",
    "name": "Complete Project Setup 7Nov",
    "created_by_uid": "17a40371-66fe-411a-963b-a977cc7cb475",
    "updated_timestamp": "2025-11-07T12:17:08.644993+00:00",
    "parentTaskId": null,
    "collaborators": [
      "17a40371-66fe-411a-963b-a977cc7cb475",
      "655a9260-f871-480f-abea-ded735b2170a"
    ],
    "pid": "352486e8-a727-470c-add4-10fe26f1fbce",
    "desc": "Optional description",
    "notes": "Optional notes",
    "priorityLevel": 5,
    "label": "bug",
    "messages": [],
    "time_entries": []
  }
}
```

### Delete Task

DELETE http://localhost:5500/{task_id}

> http://localhost:5500/5c2e225d-33af-4663-b14a-41716bfc6626

Delete a task by task ID. Only the owner of the task can delete it.  
User ID must be passed as a query parameter

Sample Request Body:
```json
{
  "task_id": "5c2e225d-33af-4663-b14a-41716bfc6626"
}

Sample Output:
```json
{
  "message": "Task deleted successfully",
  "task": {
    "id": "5c2e225d-33af-4663-b14a-41716bfc6626",
    "name": "Complete Project Setup 7Nov",
    "created_by_uid": "17a40371-66fe-411a-963b-a977cc7cb475",
    "updated_timestamp": "2025-11-07T12:17:08.644993+00:00",
    "parentTaskId": null,
    "collaborators": [
      "17a40371-66fe-411a-963b-a977cc7cb475",
      "655a9260-f871-480f-abea-ded735b2170a"
    ],
    "pid": "352486e8-a727-470c-add4-10fe26f1fbce",
    "desc": "Optional description",
    "notes": "Optional notes",
    "priorityLevel": 5,
    "label": "bug",
    "messages": [],
    "time_entries": []
  }
}
```

### Get all logs

GET http://localhost:5500/logs

> http://localhost:5500/logs

Sample Output:
```json
{
  "message": "1000 log(s) retrieved",
  "logs": [
    {
      "id": "988ce110-fabd-4979-8900-83113bb9f9c3",
      "table_name": "TASK",
      "record_id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5",
      "record_pk": {
        "id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5",
        "pid": "695d5107-0229-481a-9301-7c0562ea52d1",
        "desc": "",
        "name": "Ashtest",
        "label": "feature",
        "notes": "",
        "parentTaskId": null,
        "collaborators": [
          "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "priorityLevel": 5,
        "created_by_uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "updated_timestamp": "2025-10-21T15:38:32.194762+00:00"
      },
      "new_values": {
        "id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5",
        "pid": "695d5107-0229-481a-9301-7c0562ea52d1",
        "desc": "please don't delete me",
        "name": "Ashtest",
        "label": "feature",
        "notes": "",
        "parentTaskId": null,
        "collaborators": [
          "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "priorityLevel": 5,
        "created_by_uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "updated_timestamp": "2025-10-21T15:38:32.194762+00:00"
      },
      "changed_fields": [
        "desc"
      ],
      "delta": {
        "desc": {
          "new": "please don't delete me",
          "old": ""
        }
      },
      "user_id": null,
      "timestamp": "2025-10-23T12:00:53.403485+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "50b056ce-9370-4d1e-98d3-45aaffa2a817",
      "table_name": "TASK",
      "record_id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5",
      "record_pk": {
        "id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5",
        "pid": "695d5107-0229-481a-9301-7c0562ea52d1",
        "desc": "please don't delete me",
        "name": "Ashtest",
        "label": "feature",
        "notes": "",
        "parentTaskId": null,
        "collaborators": [
          "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "priorityLevel": 5,
        "created_by_uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "updated_timestamp": "2025-10-21T15:38:32.194762+00:00"
      },
      "new_values": {
        "id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5",
        "pid": "695d5107-0229-481a-9301-7c0562ea52d1",
        "desc": "please don't delete me",
        "name": "Ashtest",
        "label": "feature",
        "notes": "or at least ashley know, ty",
        "parentTaskId": null,
        "collaborators": [
          "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "priorityLevel": 5,
        "created_by_uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "updated_timestamp": "2025-10-21T15:38:32.194762+00:00"
      },
      "changed_fields": [
        "notes"
      ],
      "delta": {
        "notes": {
          "new": "or at least ashley know, ty",
          "old": ""
        }
      },
      "user_id": null,
      "timestamp": "2025-10-23T12:01:07.769862+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "39021388-c256-4aef-ab88-7af21825b98d",
      "table_name": "TASK",
      "record_id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5",
      "record_pk": {
        "id": "b8d51526-79e5-4daa-b73c-b0895e0a29a5"
      },
      "operation": "UPDATE",
        ....
        }
    ]

}
```

### Get logs by task id

GET http://localhost:5500/logs/{tid}

> http://localhost:5500/logs/5c2e225d-33af-4663-b14a-41716bfc6626

Sample Output:
```json
{
  "message": "Log retrieved successfully",
  "log": [
    {
      "id": "b1ada2b6-a661-4c4b-8232-1ce179d0c8f8",
      "table_name": "TASK",
      "record_id": "5c2e225d-33af-4663-b14a-41716bfc6626",
      "record_pk": {
        "id": "5c2e225d-33af-4663-b14a-41716bfc6626"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "5c2e225d-33af-4663-b14a-41716bfc6626",
        "pid": "352486e8-a727-470c-add4-10fe26f1fbce",
        "desc": "Optional description",
        "name": "Complete Project Setup 7Nov",
        "label": "bug",
        "notes": "Optional notes",
        "messages": [],
        "parentTaskId": null,
        "time_entries": [],
        "collaborators": [
          "17a40371-66fe-411a-963b-a977cc7cb475",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "priorityLevel": 5,
        "created_by_uid": "17a40371-66fe-411a-963b-a977cc7cb475",
        "updated_timestamp": "2025-11-07T12:17:08.644993+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T12:19:06.513748+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "913a6a92-d03d-42df-85b2-b91ce847928d",
      "table_name": "TASK",
      "record_id": "5c2e225d-33af-4663-b14a-41716bfc6626",
      "record_pk": {
        "id": "5c2e225d-33af-4663-b14a-41716bfc6626"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "5c2e225d-33af-4663-b14a-41716bfc6626",
        "pid": "352486e8-a727-470c-add4-10fe26f1fbce",
        "desc": "Optional description",
        "name": "New Task Title 7Nov",
        "label": "bug",
        "notes": "Optional notes",
        "messages": [],
        "parentTaskId": null,
        "time_entries": [],
        "collaborators": [
          "17a40371-66fe-411a-963b-a977cc7cb475",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "priorityLevel": 5,
        "created_by_uid": "17a40371-66fe-411a-963b-a977cc7cb475",
        "updated_timestamp": "2025-11-07T12:15:33.248458+00:00"
      },
      "new_values": {
        "id": "5c2e225d-33af-4663-b14a-41716bfc6626",
        "pid": "352486e8-a727-470c-add4-10fe26f1fbce",
        "desc": "Optional description",
        "name": "Complete Project Setup 7Nov",
        "label": "bug",
        "notes": "Optional notes",
        "messages": [],
        "parentTaskId": null,
        "time_entries": [],
        "collaborators": [
          "17a40371-66fe-411a-963b-a977cc7cb475",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "priorityLevel": 5,
        "created_by_uid": "17a40371-66fe-411a-963b-a977cc7cb475",
        "updated_timestamp": "2025-11-07T12:17:08.644993+00:00"
      },
      "changed_fields": [
        "name",
        "updated_timestamp"
      ],
      "delta": {
        "name": {
          "new": "Complete Project Setup 7Nov",
          "old": "New Task Title 7Nov"
        },
        "updated_timestamp": {
          "new": "2025-11-07T12:17:08.644993+00:00",
          "old": "2025-11-07T12:15:33.248458+00:00"
        }
      },
      "user_id": null,
      "timestamp": "2025-11-07T12:17:10.138651+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "01b8c45f-1244-4e29-8787-a1ca860c5399",
      "table_name": "TASK",
      "record_id": "5c2e225d-33af-4663-b14a-41716bfc6626",
      "record_pk": {
        "id": "5c2e225d-33af-4663-b14a-41716bfc6626"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "5c2e225d-33af-4663-b14a-41716bfc6626",
        "pid": "352486e8-a727-470c-add4-10fe26f1fbce",
        "desc": "Optional description",
        "name": "New Task Title 7Nov",
        "label": "bug",
        "notes": "Optional notes",
        "messages": [],
        "parentTaskId": null,
        "time_entries": [],
        "collaborators": [
          "17a40371-66fe-411a-963b-a977cc7cb475",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "priorityLevel": 5,
        "created_by_uid": "17a40371-66fe-411a-963b-a977cc7cb475",
        "updated_timestamp": "2025-11-07T12:15:33.248458+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T12:15:35.312283+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    }
  ]
}
```