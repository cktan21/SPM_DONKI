## Instructions
> Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 4000
```

To deactivate server:
```bash
deactivate
```
> Docker Development
```bash
docker build -t my-fastapi-app .
docker run -p 4000:4000 --name my-fastapi-container my-fastapi-app
```

## EndPoints

### Health Check

GET http://localhost:4000

Output:
```bash
"message":"Composite Manage Task Service is running 🚀","service":"manage-task-composite"
```
### Create task

POST http://127.0.0.1:4000/createTask

> http://127.0.0.1:4000/createTask

Sample Output:
```json
{
  "message": "Task created successfully via composite service",
  "task_id": "6c2c6617-971d-4c30-a0ec-263c386bc937",
  "task": {
    "message": "Task created successfully",
    "task": {
      "id": "6c2c6617-971d-4c30-a0ec-263c386bc937",
      "name": "New Task Title2",
      "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
      "updated_timestamp": "2025-09-26T00:41:00.17705+00:00",
      "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
      "collaborators": [
        "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "17a40371-66fe-411a-963b-a977cc7cb475"
      ],
      "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
      "desc": "Optional description",
      "notes": "Optional notes"
    }
  },
  "schedule": {
    "status": "failed",
    "message": "Schedule service returned 405",
    "error": "{\"detail\":\"Method Not Allowed\"}"
  },
  "project_info": {
    "message": "Project retrieved successfully",
    "project": {
      "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
      "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
      "created_at": "2025-09-14T14:08:09.069584+00:00"
    }
  },
  "collaborator_info": [
    {
      "id": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
      "auth_id": "f0ed9d08-d833-4d43-9428-41a9b179eff0",
      "email": "rc@example.com",
      "role": "user",
      "created_at": "2025-09-22T05:11:59.671524+00:00",
      "exists": true,
      "internal_api_key": "_1x2uAQdCjxcQ0GAATRigf-hPxEpQ47d7dd1y2qyu4ISiq5JZXEQNDvtGG9HgxcQH5-jjwmi_5t9tN_iWCHpV-u-0xWngN3qGsbtGMGxdpLGSVSB4cy8sdun-66XG3I4"
    },
    {
      "id": "17a40371-66fe-411a-963b-a977cc7cb475",
      "auth_id": "30397e3b-61c5-4836-98fb-987e85a8bd29",
      "email": "ashley6@example.com",
      "role": "user",
      "created_at": "2025-09-18T13:15:12.958746+00:00",
      "exists": true,
      "internal_api_key": "_1x2uAQdCjxcQ0GAATRigf-hPxEpQ47d7dd1y2qyu4ISiq5JZXEQNDvtGG9HgxcQH5-jjwmi_5t9tN_iWCHpV-u-0xWngN3qGsbtGMGxdpLGSVSB4cy8sdun-66XG3I4"
    }
  ],
  "validations_passed": {
    "parentTaskId": true,
    "collaborators": true,
    "project": true
  },
  "services_used": {
    "task_service": true,
    "schedule_service": true,
    "project_service": true,
    "users_service": true
  },
  "created_at": "2025-09-26T00:41:03.653691+00:00"
}
```

### Get task by userID

POST http://127.0.0.1:4000/tasks/{userId}

> http://127.0.0.1:4000/tasks/17a40371-66fe-411a-963b-a977cc7cb475

Sample Output:
```json
{
  "user_id": "17a40371-66fe-411a-963b-a977cc7cb475",
  "tasks": [
    {
      "task": {
        "id": "c34e506a-548b-4f05-8356-e68c11370cab",
        "name": "Update task from composite service2",
        "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
        "updated_timestamp": "2025-09-26T00:29:47.129487+00:00",
        "parentTaskId": "b1692687-4e49-41b1-bb04-3f5c18d6faf7",
        "collaborators": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
        "desc": "Set up the initial project structure and dependencies",
        "notes": "Remember to update the README file"
      },
      "schedule": {
        "message": "Task c34e506a-548b-4f05-8356-e68c11370cab Schedule Retrieved Successfully",
        "data": {
          "tid": "c34e506a-548b-4f05-8356-e68c11370cab",
          "deadline": "2024-12-31T23:59:59+00:00",
          "status": "in_progress",
          "created_at": "2025-09-20T03:08:15.62852+00:00"
        }
      },
      "project": {
        "message": "Project retrieved successfully",
        "project": {
          "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
          "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
          "created_at": "2025-09-14T14:08:09.069584+00:00",
          "name": null,
          "desc": null
        }
      }
    },
    {
      "task": {
        "id": "6c2c6617-971d-4c30-a0ec-263c386bc937",
        "name": "New Task Title2",
        "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
        "updated_timestamp": "2025-09-26T00:41:00.17705+00:00",
        "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
        "collaborators": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
        "desc": "Optional description",
        "notes": "Optional notes"
      },
      "schedule": null,
      "project": {
        "message": "Project retrieved successfully",
        "project": {
          "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
          "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
          "created_at": "2025-09-14T14:08:09.069584+00:00",
          "name": null,
          "desc": null
        }
      }
    }
  ],
  "count": 2,
  "metadata": {
    "retrieved_at": "2025-10-03T05:31:35.372119+00:00",
    "total_tasks_checked": 4
  }
}
```

### Get task by taskID

POST http://127.0.0.1:4000/tasks/{task_id}

> http://127.0.0.1:4000/tasks/17a40371-66fe-411a-963b-a977cc7cb475

Sample Output:
```json
{
  "user_id": "17a40371-66fe-411a-963b-a977cc7cb475",
  "tasks": [
    {
      "task": {
        "id": "c34e506a-548b-4f05-8356-e68c11370cab",
        "name": "Update task from composite service2",
        "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
        "updated_timestamp": "2025-09-26T00:29:47.129487+00:00",
        "parentTaskId": "b1692687-4e49-41b1-bb04-3f5c18d6faf7",
        "collaborators": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
        "desc": "Set up the initial project structure and dependencies",
        "notes": "Remember to update the README file"
      },
      "schedule": {
        "message": "Task c34e506a-548b-4f05-8356-e68c11370cab Schedule Retrieved Successfully",
        "data": {
          "tid": "c34e506a-548b-4f05-8356-e68c11370cab",
          "deadline": "2024-12-31T23:59:59+00:00",
          "status": "in_progress",
          "created_at": "2025-09-20T03:08:15.62852+00:00"
        }
      },
      "project": {
        "message": "Project retrieved successfully",
        "project": {
          "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
          "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
          "created_at": "2025-09-14T14:08:09.069584+00:00",
          "name": "software",
          "desc": null
        }
      }
    },
    {
      "task": {
        "id": "6c2c6617-971d-4c30-a0ec-263c386bc937",
        "name": "New Task Title2",
        "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
        "updated_timestamp": "2025-09-26T00:41:00.17705+00:00",
        "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
        "collaborators": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
        "desc": "Optional description",
        "notes": "Optional notes"
      },
      "schedule": null,
      "project": {
        "message": "Project retrieved successfully",
        "project": {
          "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
          "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
          "created_at": "2025-09-14T14:08:09.069584+00:00",
          "name": "software",
          "desc": null
        }
      }
    }
  ],
  "count": 2,
  "metadata": {
    "retrieved_at": "2025-10-03T05:33:15.653702+00:00",
    "total_tasks_checked": 4
  }
}
```

### Update task

PUT http://localhost:4000/{task_id}

> http://localhost:4000/c34e506a-548b-4f05-8356-e68c11370cab

Sample Output:
```json
{
  "message": "Task updated successfully via composite service",
  "task_id": "c34e506a-548b-4f05-8356-e68c11370cab",
  "validations_passed": {
    "parentTaskId": true,
    "collaborators": true,
    "project": true
  },
  "updates_applied": {
    "task_fields": [
      "name",
      "parentTaskId",
      "collaborators",
      "pid",
      "desc",
      "notes"
    ],
    "schedule_fields": [
      "status",
      "deadline"
    ]
  },
  "task": {
    "message": "Task updated successfully",
    "task": {
      "id": "c34e506a-548b-4f05-8356-e68c11370cab",
      "name": "Update task from composite service",
      "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
      "updated_timestamp": "2025-09-23T03:30:10.375276+00:00",
      "parentTaskId": "b1692687-4e49-41b1-bb04-3f5c18d6faf7",
      "collaborators": [
        "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "17a40371-66fe-411a-963b-a977cc7cb475"
      ],
      "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
      "desc": "Set up the initial project structure and dependencies",
      "notes": "Remember to update the README file"
    }
  },
  "schedule_updated": true,
  "schedule_info": {
    "status": "success",
    "message": "Task c34e506a-548b-4f05-8356-e68c11370cab schedule updated successfully",
    "data": {
      "message": "Task c34e506a-548b-4f05-8356-e68c11370cab Schedule Updated Successfully",
      "data": {
        "tid": "c34e506a-548b-4f05-8356-e68c11370cab",
        "deadline": "2024-12-31T23:59:59+00:00",
        "status": "in_progress",
        "created_at": "2025-09-20T03:08:15.62852+00:00"
      }
    }
  }
}
```

### Delete task

DELETE http://localhost:4000/{task_id}

> http://localhost:4000/67d81199-265d-423a-9998-e3955f4f58ac

Sample Output:
```json
{
  "message": "Delete workflow completed",
  "task_id": "67d81199-265d-423a-9998-e3955f4f58ac",
  "schedule_delete": {
    "url": "http://localhost:5300/67d81199-265d-423a-9998-e3955f4f58ac",
    "status_code": 404,
    "result": {
      "detail": "Task not found"
    }
  },
  "task_delete": {
    "url": "http://localhost:5500/67d81199-265d-423a-9998-e3955f4f58ac",
    "status_code": 200,
    "result": {
      "message": "Task deleted successfully",
      "task": {
        "id": "67d81199-265d-423a-9998-e3955f4f58ac",
        "name": "LET ME SLEEP PLEASE",
        "created_by_uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "updated_timestamp": "2025-09-25T19:28:05.682861+00:00",
        "parentTaskId": null,
        "collaborators": null,
        "pid": null,
        "desc": "praying rn",
        "notes": "pls work its 0330"
      }
    }
  }
}
```