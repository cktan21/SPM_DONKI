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

>Function Name

GET http://localhost:5000/recommendation/{id} //add your endpoints here

----Add Description here----

Sample Output:
```bash

```