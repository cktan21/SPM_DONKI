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

>Function Name

GET http://localhost:5200/recommendation/{id} //add your endpoints here

----Add Description here----

Sample Output:
```bash

```