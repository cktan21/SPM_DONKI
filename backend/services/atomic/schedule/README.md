## Instructions
> Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5300
```

To deactivate server:
```bash
deactivate
```
> Docker Development
```bash
docker build -t my-fastapi-app .
docker run -p 5300:5300 --name my-fastapi-container my-fastapi-app
```

## EndPoints

### Health Check

GET http://localhost:5300

Output:
```bash
"message": "Schedule Service is running 🚀😌"
```

### Get Schedule w Task ID

GET http://localhost:5300/{task_id}

> http://localhost:5300/b1692687-4e49-41b1-bb04-3f5c18d6faf7

Sample Output:
```json
{
	"message": "Task b1692687-4e49-41b1-bb04-3f5c18d6faf7 Schedule Retrieved Successfully",
	"data": {
		"tid": "b1692687-4e49-41b1-bb04-3f5c18d6faf7",
		"deadline": "2025-09-18T16:00:00+00:00",
		"status": "ongoing",
		"created_at": "2025-09-14T14:07:44.741812+00:00"
	}
}
```

### Insert New Schedule

POST http://localhost:5300

> http://localhost:5300

Sample Input:
```json
{
    "tid": "c34e506a-548b-4f05-8356-e68c11370cab",
    "deadline": "2025-09-26T15:42:21Z",
}
```

Sample Output:
```json
{
	"message": "Task c34e506a-548b-4f05-8356-e68c11370cab Schedule Inserted Successfully",
	"data": {
		"tid": "c34e506a-548b-4f05-8356-e68c11370cab",
		"deadline": "2025-09-26T15:42:21+00:00",
		"status": "ongoing",
		"created_at": "2025-09-20T03:08:15.62852+00:00"
	}
}
```

### Note:
- New Schedule status is always assumed to be `ongoing` hence not requiring a field
- **One** Task can only have *ONE entry* in schedule
    - adding a task when the task_id already exist will result in error


### Update Existing Schedule

PUT http://localhost:5300

> http://localhost:5300/b1692687-4e49-41b1-bb04-3f5c18d6faf7

Sample Input:
```json
{
    "status": "overdue",
    "deadline": "2025-10-11T11:58:20+08:00"
}
```

Sample Output:
```json
{
	"message": "Task c34e506a-548b-4f05-8356-e68c11370cab Schedule Updated Successfully",
	"data": {
		"tid": "c34e506a-548b-4f05-8356-e68c11370cab",
		"deadline": "2025-09-26T15:42:21+00:00",
		"status": "overdue",
		"created_at": "2025-09-20T03:08:15.62852+00:00"
	}
}
```

### Note:
- `task_id` has to exist in the db otherwise it will return an error
- `status` and `deadline` are not mandatory fields, you can change one without changing the other
    - eg: `{"status": "overdue"}` and `{"deadline": "2025-10-11T11:58:20+08:00"}` both valid inputs


### Delete Schedule w Task ID

GET http://localhost:5300/{task_id}

> http://localhost:5300/b1692687-4e49-41b1-bb04-3f5c18d6faf7

Sample Output:
```json
{
	"message": "Task c34e506a-548b-4f05-8356-e68c11370cab deleted successfully"
}
```