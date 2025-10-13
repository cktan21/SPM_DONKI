## Instructions

> Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5200
```

To deactivate server:

```bash
deactivate
```

> Docker Development

```bash
docker build -t my-fastapi-app .
docker run -p 5200:5200 --name my-fastapi-container my-fastapi-app
```

## EndPoints

### Health Check

GET http://localhost:5200

Output:

```bash
"message": "Project Service is running 🚀😫"
```

### Get project by project ID

GET http://localhost:5200/pid/{project_id}

> http://localhost:5200/pid/40339da5-9a62-4195-bbe5-c69f2fc04ed6

Sample Output:

```json
{
    "message": "Project with Project ID 40339da5-9a62-4195-bbe5-c69f2fc04ed6 retrieved successfully",
    "project": {
        "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
        "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
        "created_at": "2025-09-14T14:08:09.069584+00:00",
        "name": "software",
        "desc": null
    }
}
```

### Get project by Owner UID

GET http://localhost:5200/uid/{user_id}

> http://localhost:5200/uid/fc001efc-0e9c-4700-a041-e914f6d9d101

Sample Output:

```json
{
    "message": "Projects with user id fc001efc-0e9c-4700-a041-e914f6d9d101 retrieved successfully",
    "project": [
        {
            "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
            "created_at": "2025-09-14T14:08:09.069584+00:00",
            "name": "software",
            "desc": null
        },
        {
            "id": "8009a599-d211-4bcf-baa5-877a19967b10",
            "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
            "created_at": "2025-10-10T04:49:52.240582+00:00",
            "name": "some shit",
            "desc": "hahah"
        }
    ]
}
```

### Insert new Project

POST http://localhost:5200

> http://localhost:5200

Sample Input:

```json
{
    "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
    "name": "SPM",
    "desc": "heeheehahha" //optional
}
```

Sample Output:

```json
{
    "message": "Project Inserted Successfully",
    "data": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
        "created_at": "2025-10-10T05:06:38.602368+00:00",
        "name": "SPM",
        "desc": "heeheehahha"
    }
}
```

### Note:

-   `desc` field is optional
-   there can be multiple projects with the same name
    -   might wanna restrict this on the db side to ensure one person cannot have a project with the same name LOL

### Update Existing Project Details

PUT http://localhost:5200/{project_id}

> http://localhost:5200/8009a599-d211-4bcf-baa5-877a19967b10

Sample Input:

```json
{
    "uid": "765bc84f-eba5-4d32-987b-d55adef7fe65",
    "name": "overdue",
    "desc": "tough"
}
```

Sample Output:

```json
{
    "message": "Project 8009a599-d211-4bcf-baa5-877a19967b10 Project Updated Successfully",
    "data": {
        "id": "8009a599-d211-4bcf-baa5-877a19967b10",
        "uid": "765bc84f-eba5-4d32-987b-d55adef7fe65",
        "created_at": "2025-10-10T04:49:52.240582+00:00",
        "name": "overdue",
        "desc": "tough"
    }
}
```

### Note:

-   `project_id` has to exist in the db otherwise it will return an error
-   `uid`, `name` and `desc` are not mandatory fields, you can change one without changing the other
    -   eg: `{"uid": "765bc84f-eba5-4d32-987b-d55adef7fe65"}`, `{"name": "overdue"}`, `{"desc": "tough"}` and any combination of the 3 are valid inputs

### Delete Schedule w Task ID

DELETE http://localhost:5200/{project_id}

> http://localhost:5200/8009a599-d211-4bcf-baa5-877a19967b10

Sample Output:

```json
{
    "message": "Project 8009a599-d211-4bcf-baa5-877a19967b10 deleted successfully"
}
```
