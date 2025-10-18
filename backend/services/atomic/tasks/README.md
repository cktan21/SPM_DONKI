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

> http://localhost:5500/b1692687-4e49-41b1-bb04-3f5c18d6faf7

Sample Output:
```json
{
    "message": "Task retrieved successfully",
    "task": {
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
}
```

### Get task by project ID

GET http://localhost:5500/pid/{project_id}

> http://localhost:5500/pid/40339da5-9a62-4195-bbe5-c69f2fc04ed6

Sample Output:
```json
{
    "message": "2 task(s) retrieved",
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
    "name": "New Task Title",
    "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
    "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
    "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
    "collaborators": [
        "3e3b2d6c-6d6b-4dc0-9b76-0b6b3fe9c001",
        "f7f5cf6e-1c3a-4d3a-8d50-5a2f60d9a002"
    ],
    "desc": "Optional description",
    "notes": "Optional notes"
}

Sample Output:
```json
{
    "message": "Task created successfully",
    "task": {
        "id": "5c8cf645-4328-4f92-89f7-25fd29efeb21",
        "name": "New Task Title",
        "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
        "updated_timestamp": "2025-09-16T16:54:30.006993+00:00",
        "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
        "collaborators": [
            "3e3b2d6c-6d6b-4dc0-9b76-0b6b3fe9c001",
            "f7f5cf6e-1c3a-4d3a-8d50-5a2f60d9a002"
        ],
        "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
        "desc": "Optional description",
        "notes": "Optional notes"
    }
}
```

### Update Task

PUT http://localhost:5500/{task_id}

Update task details by task id

Sample Output:
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": "c34e506a-548b-4f05-8356-e68c11370cab",
    "name": "Complete Project Setup hohohohoho",
    "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
    "updated_timestamp": "2025-09-16T16:55:48.563092+00:00",
    "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
    "collaborators": [
      "3e3b2d6c-6d6b-4dc0-9b76-0b6b3fe9c001",
      "f7f5cf6e-1c3a-4d3a-8d50-5a2f60d9a002"
    ],
    "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
    "desc": "Set up the initial project structure and dependencies",
    "notes": "Remember to update the README file"
  }
}
```

### Delete Task

DELETE http://localhost:5500/tasks/{task_id}?user_id=<user_id>

Delete a task by task ID. Only the owner of the task can delete it.  
User ID must be passed as a query parameter

Sample Request Body:
```json
{
  "user_id": "7b055ff5-84f4-47bc-be7d-5905caec3ec6"
}

Sample Output:
```json
{
  "message": "Task deleted successfully",
  "task": {
    "id": "bbdfaf7d-448b-491b-8179-daa28640774e",
    "name": "New Task Title",
    "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
    "updated_timestamp": "2025-09-16T16:54:30.006993+00:00",
    "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
    "collaborators": [
      "3e3b2d6c-6d6b-4dc0-9b76-0b6b3fe9c001",
      "f7f5cf6e-1c3a-4d3a-8d50-5a2f60d9a002"
    ],
    "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
    "desc": "Optional description",
    "notes": "Optional notes"
  }
}
