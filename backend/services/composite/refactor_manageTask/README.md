## Instructions
> Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5800
```

To deactivate server:
```bash
deactivate
```
> Docker Development
```bash
docker build -t my-fastapi-app .
docker run -p 5800:5800 --name my-fastapi-container my-fastapi-app
```

## EndPoints

### Health Check

GET http://localhost:5800

Output:
```bash
"message":"Composite REFACTORED Manage Task Service is running 🚀","service":"refactor-manage-task-composite"
```
### Create task

POST http://127.0.0.1:5800/{task_id}

> http://localhost:5800/0a4771b4-5f73-4c3a-9a82-0b442caec82a

Sample Output:
```json
{
  "message": "Delete workflow completed and project members synced",
  "task_id": "0a4771b4-5f73-4c3a-9a82-0b442caec82a",
  "task_delete": {
    "url": "http://tasks:5500/0a4771b4-5f73-4c3a-9a82-0b442caec82a",
    "status_code": 200,
    "result": {
      "message": "Task deleted successfully",
      "task": {
        "id": "0a4771b4-5f73-4c3a-9a82-0b442caec82a",
        "name": "INTSeedUpdateTest20251107T003845Z",
        "created_by_uid": "655a9260-f871-480f-abea-ded735b2170a",
        "updated_timestamp": "2025-11-07T00:38:45.61106+00:00",
        "parentTaskId": null,
        "collaborators": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "pid": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "desc": "seed for update tests",
        "notes": null,
        "priorityLevel": 2,
        "label": "seed",
        "messages": [],
        "time_entries": []
      }
    }
  },
  "members_sync": {
    "project_id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
    "checked_users": [
      "655a9260-f871-480f-abea-ded735b2170a",
      "fb892a63-2401-46fc-b660-bf3fe1196d4e"
    ]
  }
}
``