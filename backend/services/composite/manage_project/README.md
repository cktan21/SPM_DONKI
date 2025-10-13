## Instructions
> Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 4100
```

To deactivate server:
```bash
deactivate
```
> Docker Development
```bash
docker build -t my-fastapi-app .
docker run -p 4100:4100 --name my-fastapi-container my-fastapi-app
```

## EndPoints

### Health Check

GET http://localhost:4100

Output:
```bash
"message":"Composite Manage Task Service is running 🚀","service":"manage-task-composite"
```

### Get Projects by User ID

POST http://127.0.0.1:4100/uid/{user_id}

> http://127.0.0.1:4100/uid/fc001efc-0e9c-4700-a041-e914f6d9d101

Sample Output:
```json
{
    "message": "Projects retrieved successfully",
    "user_id": "fc001efc-0e9c-4700-a041-e914f6d9d101",
    "projects": [
        {
            "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
            "created_at": "2025-09-14T14:08:09.069584+00:00",
            "name": "software",
            "desc": null,
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
        },
        {
            "id": "01dd2989-eb1c-4729-80bd-1cb046e4799b",
            "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
            "created_at": "2025-10-10T05:05:37.144401+00:00",
            "name": "SPM",
            "desc": null,
            "tasks": []
        }
    ]
}
```

### Get Project by Project ID

POST http://127.0.0.1:4100/pid/{project_id}

> http://127.0.0.1:4100/pid/40339da5-9a62-4195-bbe5-c69f2fc04ed6

Sample Output:
```json
{
    "message": "Project retrieved successfully",
    "project_id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
    "project": {
        "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
        "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
        "created_at": "2025-09-14T14:08:09.069584+00:00",
        "name": "software",
        "desc": null,
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
            },
            {
                "id": "33949f99-20d0-423d-9b26-f09292b2e40d",
                "name": "get coffee2",
                "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
                "updated_timestamp": "2025-10-05T22:06:06.665826+00:00",
                "parentTaskId": null,
                "collaborators": null,
                "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
                "desc": "Optional description",
                "notes": "Optional notes",
                "priorityLevel": 5,
                "priorityLabel": "Medium"
            }
        ]
    }
}
```

