## Instructions
> Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5100
```

To deactivate server:
```bash
deactivate
```
> Docker Development
```bash
docker build -t my-fastapi-app .
docker run -p 5100:5100 --name my-fastapi-container my-fastapi-app
```

## EndPoints

### Health Check

GET http://localhost:5100

Output:
```bash
"message": "User Service is running 🚀🥺"
```

>### Get user by user ID (for internal validation use)

GET http://localhost:5100/internal/{task_id}

> http://127.0.0.1:5100/internal/0ec8a99d-3aab-4ec6-b692-fda88656844f

Sample Output:
```json
{
  "id": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
  "auth_id": "f0ed9d08-d833-4d43-9428-41a9b179eff0",
  "email": "rc@example.com",
  "role": "user",
  "created_at": "2025-09-22T05:11:59.671524+00:00",
  "exists": true,
  "internal_api_key": "secret"
}
```