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

>### Get project by project ID

GET http://localhost:5200/{project_id}

> http://localhost:5200/40339da5-9a62-4195-bbe5-c69f2fc04ed6

Sample Output:
```json
{
  "message": "Project retrieved successfully",
  "project": {
    "id": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
    "uid": "fc001efc-0e9c-4700-a041-e914f6d9d101",
    "created_at": "2025-09-14T14:08:09.069584+00:00"
  }
}