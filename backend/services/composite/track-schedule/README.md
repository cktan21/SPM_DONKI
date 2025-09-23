## Instructions
> Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5600
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

GET http://localhost:5600

Output:
```bash
"message":"Composite Task Update Service is running 🚀","service":"track-schedule-composite"
```
>### Update task

PUT http://localhost:5600/{task_id}

> http://localhost:5500/c34e506a-548b-4f05-8356-e68c11370cab

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