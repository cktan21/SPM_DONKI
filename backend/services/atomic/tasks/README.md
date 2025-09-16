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

>### Create Task

POST http://localhost:5500/tasks

Create a new task

Sample Output:
```bash
{
  "message": "Task created successfully",
  "task": {
    "id": "5c8cf645-4328-4f92-89f7-25fd29efeb21",
    "name": "New Task Title",
    "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
    "updated_timestamp": "2025-09-16T16:54:30.006993+00:00",
    "parentTaskId": null,
    "collaborators": null,
    "pid": null,
    "desc": "Optional description",
    "notes": "Optional notes"
  }
}
```

>### Update Task

PUT http://localhost:5500/{task_id}

Update task details by task id

Sample Output:
```bash
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