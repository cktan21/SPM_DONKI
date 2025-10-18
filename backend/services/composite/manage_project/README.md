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
                    "id": "04213807-bc3a-4f62-ae6d-e81ab3d458ab",
                    "name": "wfwejfoiewjfow",
                    "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
                    "updated_timestamp": "2025-10-17T05:08:40.110212+00:00",
                    "parentTaskId": "33949f99-20d0-423d-9b26-f09292b2e40d",
                    "collaborators": [
                        "655a9260-f871-480f-abea-ded735b2170a",
                        "fb892a63-2401-46fc-b660-bf3fe1196d4e"
                    ],
                    "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
                    "desc": "Optional description",
                    "notes": "Optional notes",
                    "priorityLevel": 5,
                    "priorityLabel": "Medium",
                    "deadline": "2025-12-31T23:59:59+00:00",
                    "status": "ongoing",
                    "is_recurring": false,
                    "next_occurrence": null,
                    "start": "2025-10-18T06:43:45.397511+00:00",
                    "sid": "264ad005-c0cc-48ae-8315-1d15c5a5af18"
                },
                {
                    "id": "be238e36-2506-432a-a267-e2a1308ff22b",
                    "name": "New Task Title2",
                    "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
                    "updated_timestamp": "2025-10-17T07:41:56.373682+00:00",
                    "parentTaskId": "33949f99-20d0-423d-9b26-f09292b2e40d",
                    "collaborators": [
                        "655a9260-f871-480f-abea-ded735b2170a",
                        "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
                        "fb892a63-2401-46fc-b660-bf3fe1196d4e"
                    ],
                    "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
                    "desc": "Optional description",
                    "notes": "Optional notes",
                    "priorityLevel": 5,
                    "priorityLabel": "Medium",
                    "deadline": "2025-10-31T18:40:00+00:00",
                    "status": "ongoing",
                    "is_recurring": false,
                    "next_occurrence": null,
                    "start": "2025-10-18T06:43:45.397511+00:00",
                    "sid": "0e476bff-bee6-4cab-b734-841832ebbd64"
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
                "id": "04213807-bc3a-4f62-ae6d-e81ab3d458ab",
                "name": "wfwejfoiewjfow",
                "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
                "updated_timestamp": "2025-10-17T05:08:40.110212+00:00",
                "parentTaskId": "33949f99-20d0-423d-9b26-f09292b2e40d",
                "collaborators": [
                    "655a9260-f871-480f-abea-ded735b2170a",
                    "fb892a63-2401-46fc-b660-bf3fe1196d4e"
                ],
                "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
                "desc": "Optional description",
                "notes": "Optional notes",
                "priorityLevel": 5,
                "priorityLabel": "Medium",
                "deadline": "2025-12-31T23:59:59+00:00",
                "status": "ongoing",
                "is_recurring": false,
                "next_occurrence": null,
                "start": "2025-10-18T06:43:45.397511+00:00",
                "sid": "264ad005-c0cc-48ae-8315-1d15c5a5af18"
            },
            {
                "id": "be238e36-2506-432a-a267-e2a1308ff22b",
                "name": "New Task Title2",
                "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
                "updated_timestamp": "2025-10-17T07:41:56.373682+00:00",
                "parentTaskId": "33949f99-20d0-423d-9b26-f09292b2e40d",
                "collaborators": [
                    "655a9260-f871-480f-abea-ded735b2170a",
                    "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
                    "fb892a63-2401-46fc-b660-bf3fe1196d4e"
                ],
                "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
                "desc": "Optional description",
                "notes": "Optional notes",
                "priorityLevel": 5,
                "priorityLabel": "Medium",
                "deadline": "2025-10-31T18:40:00+00:00",
                "status": "ongoing",
                "is_recurring": false,
                "next_occurrence": null,
                "start": "2025-10-18T06:43:45.397511+00:00",
                "sid": "0e476bff-bee6-4cab-b734-841832ebbd64"
            }
        ]
    }
}
```

