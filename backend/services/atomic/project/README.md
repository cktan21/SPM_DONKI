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

## Access API docs at: http://localhost:5200/docs#

### Health Check

GET http://localhost:5200

Output:

```bash
"message": "Project Service is running 🚀😫"
```

### Get all projects

GET http://localhost:5200/all

> http://localhost:5200/all

Sample Output:

```json
{
  "message": "11 project(s) retrieved",
  "project": [
    {
      "name": "Create email reminder functionality",
      "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
      "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
      "members": [
        "655a9260-f871-480f-abea-ded735b2170a",
        "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
      ],
      "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
      "created_at": "2025-10-13T12:35:02.560190Z",
      "updated_at": null
    },
    {
      "name": "AI Chat Application",
      "desc": "A real-time chat application powered by AI",
      "uid": "655a9260-f871-480f-abea-ded735b2170a",
      "members": [
        "655a9260-f871-480f-abea-ded735b2170a",
        "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "0ec8a99d-3aab-4ec6-b692-fda88656844f"
      ],
      "id": "ccfcfc03-d00a-4732-b8f7-99019000670b",
      "created_at": "2025-10-24T06:06:24.593428Z",
      "updated_at": null
    },
    {
      "name": "TESTING PLS DONT AMEND",
      "desc": "bros i cant find the btn",
      "uid": "655a9260-f871-480f-abea-ded735b2170a",
      "members": [
        "655a9260-f871-480f-abea-ded735b2170a",
        "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "6933d965-e4c4-4b49-bc99-08236b1d9458",
        "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "944d73be-9625-4fd1-8c6a-00e161da0642",
        "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
      ],
      "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
      "created_at": "2025-11-04T20:29:54.315946Z",
      "updated_at": null
    },
    {
      "name": "TESTING JW CY DONT AMEND",
      "desc": "bros i cant find the btn",
      "uid": "655a9260-f871-480f-abea-ded735b2170a",
      "members": [
        "655a9260-f871-480f-abea-ded735b2170a",
        "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
        "944d73be-9625-4fd1-8c6a-00e161da0642",
        "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "6933d965-e4c4-4b49-bc99-08236b1d9458"
      ],
      "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
      "created_at": "2025-11-06T22:07:01.818074Z",
      "updated_at": null
    },
    {
      "name": "testname",
      "desc": "testing audit trail",
      "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
      "members": [
        "944d73be-9625-4fd1-8c6a-00e161da0642",
        "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "0ec8a99d-3aab-4ec6-b692-fda88656844f"
      ],
      "id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "created_at": "2025-10-23T11:03:47.431495Z",
      "updated_at": null
    },
    {
      "name": "Revamp Authenthication",
      "desc": "This project aims to recreate the authenthication, to make the app more secure",
      "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
      "members": [
        "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "944d73be-9625-4fd1-8c6a-00e161da0642"
      ],
      "id": "695d5107-0229-481a-9301-7c0562ea52d1",
      "created_at": "2025-10-10T05:06:38.602368Z",
      "updated_at": null
    },
    {
      "name": "manager test",
      "desc": "desc manager test",
      "uid": "655a9260-f871-480f-abea-ded735b2170a",
      "members": [
        "944d73be-9625-4fd1-8c6a-00e161da0642",
        "da283ea9-552d-48dd-be56-18c81364adf0",
        "655a9260-f871-480f-abea-ded735b2170a"
      ],
      "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
      "created_at": "2025-10-19T10:49:39.934347Z",
      "updated_at": null
    },
    {
      "name": "itest-all-1",
      "desc": null,
      "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "members": [],
      "id": "1ebfba1a-afa0-4bc0-9cc3-1bfd0f7acad7",
      "created_at": "2025-11-07T01:29:40.480486Z",
      "updated_at": null
    },
    {
      "name": "Delete this project",
      "desc": "Xian xia",
      "uid": "655a9260-f871-480f-abea-ded735b2170a",
      "members": [
        "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "655a9260-f871-480f-abea-ded735b2170a",
        "17a40371-66fe-411a-963b-a977cc7cb475",
        "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
        "944d73be-9625-4fd1-8c6a-00e161da0642",
        "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "6933d965-e4c4-4b49-bc99-08236b1d9458"
      ],
      "id": "352486e8-a727-470c-add4-10fe26f1fbce",
      "created_at": "2025-10-25T10:03:48.066105Z",
      "updated_at": null
    },
    {
      "name": "itest-all-2",
      "desc": null,
      "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "members": [],
      "id": "2644b4c6-61e1-48d2-9531-1df42142b3f7",
      "created_at": "2025-11-07T01:29:40.816691Z",
      "updated_at": null
    },
    {
      "name": "itest-dept",
      "desc": null,
      "uid": "655a9260-f871-480f-abea-ded735b2170a",
      "members": [],
      "id": "addb49bd-fdcb-43e1-9564-b2a25ae998bb",
      "created_at": "2025-11-07T02:35:55.131350Z",
      "updated_at": null
    }
  ]
}
```

### Get projects by department

GET http://localhost:5200/dept/{department}

> http://localhost:5200/dept/HR

Sample Output:

```json
{
  "message": "3 project(s) retrieved for department 'HR'",
  "project": [
    {
      "name": "testname",
      "desc": "testing audit trail",
      "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
      "members": [
        "944d73be-9625-4fd1-8c6a-00e161da0642",
        "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "0ec8a99d-3aab-4ec6-b692-fda88656844f"
      ],
      "id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "created_at": "2025-10-23T11:03:47.431495Z",
      "updated_at": null
    },
    {
      "name": "itest-all-1",
      "desc": null,
      "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "members": [],
      "id": "1ebfba1a-afa0-4bc0-9cc3-1bfd0f7acad7",
      "created_at": "2025-11-07T01:29:40.480486Z",
      "updated_at": null
    },
    {
      "name": "itest-all-2",
      "desc": null,
      "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "members": [],
      "id": "2644b4c6-61e1-48d2-9531-1df42142b3f7",
      "created_at": "2025-11-07T01:29:40.816691Z",
      "updated_at": null
    }
  ]
}
```

### Get project by project ID

GET http://localhost:5200/pid/{project_id}

> http://localhost:5200/pid/7f233f02-561e-4ada-9ecc-2f39320ee022

Sample Output:

```json
{
  "message": "Project with Project ID 7f233f02-561e-4ada-9ecc-2f39320ee022 retrieved successfully",
  "project": {
    "name": "TESTING PLS DONT AMEND",
    "desc": "bros i cant find the btn",
    "uid": "655a9260-f871-480f-abea-ded735b2170a",
    "members": [
      "655a9260-f871-480f-abea-ded735b2170a",
      "fb892a63-2401-46fc-b660-bf3fe1196d4e",
      "6933d965-e4c4-4b49-bc99-08236b1d9458",
      "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "bba910a9-1685-4fa3-af21-ccb2e11cf751",
      "944d73be-9625-4fd1-8c6a-00e161da0642",
      "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
    ],
    "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
    "created_at": "2025-11-04T20:29:54.315946Z",
    "updated_at": null
  },
  "data": null
}
```

### Get project by user ID

GET http://localhost:5200/uid/{user_id}

> http://localhost:5200/uid/d568296e-3644-4ac0-9714-dcaa0aaa5fb0

Sample Output:

```json
{
  "message": "Projects with user id d568296e-3644-4ac0-9714-dcaa0aaa5fb0 retrieved successfully",
  "project": [
    {
      "name": "itest-all-1",
      "desc": null,
      "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "members": [],
      "id": "1ebfba1a-afa0-4bc0-9cc3-1bfd0f7acad7",
      "created_at": "2025-11-07T01:29:40.480486Z",
      "updated_at": null
    },
    {
      "name": "itest-all-2",
      "desc": null,
      "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "members": [],
      "id": "2644b4c6-61e1-48d2-9531-1df42142b3f7",
      "created_at": "2025-11-07T01:29:40.816691Z",
      "updated_at": null
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
    "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
    "name": "SPM",
    "desc": "heeheehahha" //optional
}
```

Sample Output:

```json
{
  "message": "Project Inserted Successfully",
  "project": {
    "name": "SPM",
    "desc": "heeheehahha",
    "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
    "members": [],
    "id": "6238490f-1a23-4613-9a6d-d45ed902255b",
    "created_at": "2025-11-07T11:41:57.419980Z",
    "updated_at": null
  },
  "data": {
    "id": "6238490f-1a23-4613-9a6d-d45ed902255b",
    "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
    "created_at": "2025-11-07T11:41:57.41998+00:00",
    "name": "SPM",
    "desc": "heeheehahha",
    "members": []
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
  "message": "Project 6238490f-1a23-4613-9a6d-d45ed902255b Project Updated Successfully",
  "project": {
    "name": "overdue",
    "desc": "tough",
    "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
    "members": [],
    "id": "6238490f-1a23-4613-9a6d-d45ed902255b",
    "created_at": "2025-11-07T11:41:57.419980Z",
    "updated_at": null
  },
  "data": {
    "id": "6238490f-1a23-4613-9a6d-d45ed902255b",
    "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
    "created_at": "2025-11-07T11:41:57.41998+00:00",
    "name": "overdue",
    "desc": "tough",
    "members": []
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

### Get all logs

GET 'http://localhost:5200/logs

> http://localhost:5200/logs

Sample Output:

```json
{
  "message": "366 log(s) retrieved",
  "logs": [
    {
      "id": "139b4e3c-e30e-40af-b750-3403fdedc533",
      "table_name": "PROJECT",
      "record_id": "6238490f-1a23-4613-9a6d-d45ed902255b",
      "record_pk": {
        "id": "6238490f-1a23-4613-9a6d-d45ed902255b"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "6238490f-1a23-4613-9a6d-d45ed902255b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "tough",
        "name": "overdue",
        "members": [],
        "created_at": "2025-11-07T11:41:57.41998+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T11:44:02.63427+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6c75bf75-dd7a-4a26-b08b-d272da8d4bf2",
      "table_name": "PROJECT",
      "record_id": "6238490f-1a23-4613-9a6d-d45ed902255b",
      "record_pk": {
        "id": "6238490f-1a23-4613-9a6d-d45ed902255b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "6238490f-1a23-4613-9a6d-d45ed902255b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "heeheehahha",
        "name": "SPM",
        "members": [],
        "created_at": "2025-11-07T11:41:57.41998+00:00"
      },
      "new_values": {
        "id": "6238490f-1a23-4613-9a6d-d45ed902255b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "tough",
        "name": "overdue",
        "members": [],
        "created_at": "2025-11-07T11:41:57.41998+00:00"
      },
      "changed_fields": [
        "desc",
        "name"
      ],
      "delta": {
        "desc": {
          "new": "tough",
          "old": "heeheehahha"
        },
        "name": {
          "new": "overdue",
          "old": "SPM"
        }
      },
      "user_id": null,
      "timestamp": "2025-11-07T11:43:38.86081+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "486ed0ee-cbf0-4ad5-aa58-6839d137886b",
      "table_name": "PROJECT",
      "record_id": "6238490f-1a23-4613-9a6d-d45ed902255b",
      "record_pk": {
        "id": "6238490f-1a23-4613-9a6d-d45ed902255b"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "6238490f-1a23-4613-9a6d-d45ed902255b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "heeheehahha",
        "name": "SPM",
        "members": [],
        "created_at": "2025-11-07T11:41:57.41998+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T11:41:57.41998+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "dd955441-0c8d-458a-82e0-d5536c32b26a",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-07T05:38:54.538247+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9712ae59-c2ac-492f-af26-eab8665fc4f9",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751"
          ],
          "old": [
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-07T03:19:51.442399+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ac06f624-6245-477c-8910-ac2392cdaa16",
      "table_name": "PROJECT",
      "record_id": "1a4859bd-801c-4c0c-80c3-9a0de064c387",
      "record_pk": {
        "id": "1a4859bd-801c-4c0c-80c3-9a0de064c387"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "1a4859bd-801c-4c0c-80c3-9a0de064c387",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T03:10:08.388539+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:10:42.566818+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4718cb9b-b378-43df-bb34-563c80554254",
      "table_name": "PROJECT",
      "record_id": "1a4859bd-801c-4c0c-80c3-9a0de064c387",
      "record_pk": {
        "id": "1a4859bd-801c-4c0c-80c3-9a0de064c387"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "1a4859bd-801c-4c0c-80c3-9a0de064c387",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T03:10:08.388539+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:10:08.388539+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d97467a7-0c42-4537-a282-ba65328f6da4",
      "table_name": "PROJECT",
      "record_id": "2956aaf4-edbe-45c0-be6c-531993b71900",
      "record_pk": {
        "id": "2956aaf4-edbe-45c0-be6c-531993b71900"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "2956aaf4-edbe-45c0-be6c-531993b71900",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T03:09:55.120798+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:10:07.005263+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e7440d6b-883b-4739-9912-ceed09739398",
      "table_name": "PROJECT",
      "record_id": "2956aaf4-edbe-45c0-be6c-531993b71900",
      "record_pk": {
        "id": "2956aaf4-edbe-45c0-be6c-531993b71900"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "2956aaf4-edbe-45c0-be6c-531993b71900",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T03:09:55.120798+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:09:55.120798+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "955f39d6-8a65-4428-8672-9e7c75194abe",
      "table_name": "PROJECT",
      "record_id": "791c2af7-4a2d-42f4-8df1-199330eb407f",
      "record_pk": {
        "id": "791c2af7-4a2d-42f4-8df1-199330eb407f"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "791c2af7-4a2d-42f4-8df1-199330eb407f",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T03:08:51.985565+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:09:54.009492+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "2a15040f-688c-4192-81d6-342e594dab18",
      "table_name": "PROJECT",
      "record_id": "10c541b7-45fa-40ed-be0f-4c1d65d0022f",
      "record_pk": {
        "id": "10c541b7-45fa-40ed-be0f-4c1d65d0022f"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "10c541b7-45fa-40ed-be0f-4c1d65d0022f",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T03:08:52.295113+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:09:53.426935+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "538cf5f1-bb7d-4e0f-b903-a61093ed6734",
      "table_name": "PROJECT",
      "record_id": "10c541b7-45fa-40ed-be0f-4c1d65d0022f",
      "record_pk": {
        "id": "10c541b7-45fa-40ed-be0f-4c1d65d0022f"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "10c541b7-45fa-40ed-be0f-4c1d65d0022f",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T03:08:52.295113+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:08:52.295113+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "86492d2f-d46c-4ed3-b608-457a730fa825",
      "table_name": "PROJECT",
      "record_id": "791c2af7-4a2d-42f4-8df1-199330eb407f",
      "record_pk": {
        "id": "791c2af7-4a2d-42f4-8df1-199330eb407f"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "791c2af7-4a2d-42f4-8df1-199330eb407f",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T03:08:51.985565+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:08:51.985565+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4e43296c-369a-4429-a3d8-920d450ef3fb",
      "table_name": "PROJECT",
      "record_id": "d498ad7f-ebe3-43b7-8b36-85c48982bc61",
      "record_pk": {
        "id": "d498ad7f-ebe3-43b7-8b36-85c48982bc61"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "d498ad7f-ebe3-43b7-8b36-85c48982bc61",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T03:08:39.626861+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:08:51.167706+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "97cf6491-ff06-49a8-b62f-a21ac88fc954",
      "table_name": "PROJECT",
      "record_id": "d48ae6b3-4e14-41e5-adef-853ddd02d1f8",
      "record_pk": {
        "id": "d48ae6b3-4e14-41e5-adef-853ddd02d1f8"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "d48ae6b3-4e14-41e5-adef-853ddd02d1f8",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T03:08:39.93779+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:08:50.876646+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9a4cbb8e-bc60-4c8b-ba34-7b8d716ed8ee",
      "table_name": "PROJECT",
      "record_id": "d48ae6b3-4e14-41e5-adef-853ddd02d1f8",
      "record_pk": {
        "id": "d48ae6b3-4e14-41e5-adef-853ddd02d1f8"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "d48ae6b3-4e14-41e5-adef-853ddd02d1f8",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T03:08:39.93779+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:08:39.93779+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4cee9bb7-d670-4bdd-ae5c-4d6d37897717",
      "table_name": "PROJECT",
      "record_id": "d498ad7f-ebe3-43b7-8b36-85c48982bc61",
      "record_pk": {
        "id": "d498ad7f-ebe3-43b7-8b36-85c48982bc61"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "d498ad7f-ebe3-43b7-8b36-85c48982bc61",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T03:08:39.626861+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:08:39.626861+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "214f25ff-51c7-4544-a107-14d3d0660d05",
      "table_name": "PROJECT",
      "record_id": "ebdbe87f-861b-4fe0-a29c-222e5c44b8d8",
      "record_pk": {
        "id": "ebdbe87f-861b-4fe0-a29c-222e5c44b8d8"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "ebdbe87f-861b-4fe0-a29c-222e5c44b8d8",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T03:05:16.986165+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:05:17.052422+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "560605ef-003b-4b88-9df2-c03ccd8571a7",
      "table_name": "PROJECT",
      "record_id": "ebdbe87f-861b-4fe0-a29c-222e5c44b8d8",
      "record_pk": {
        "id": "ebdbe87f-861b-4fe0-a29c-222e5c44b8d8"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "ebdbe87f-861b-4fe0-a29c-222e5c44b8d8",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T03:05:16.986165+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:05:16.986165+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "129753cc-6e50-43a1-9aeb-f213b3fb8a1e",
      "table_name": "PROJECT",
      "record_id": "2dcc2a8b-5d28-4c4e-a9b7-fc239993fa89",
      "record_pk": {
        "id": "2dcc2a8b-5d28-4c4e-a9b7-fc239993fa89"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "2dcc2a8b-5d28-4c4e-a9b7-fc239993fa89",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T03:04:53.407527+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:05:15.907294+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6fc7251b-fd18-4c88-8255-fbc4dcea23b8",
      "table_name": "PROJECT",
      "record_id": "2dcc2a8b-5d28-4c4e-a9b7-fc239993fa89",
      "record_pk": {
        "id": "2dcc2a8b-5d28-4c4e-a9b7-fc239993fa89"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "2dcc2a8b-5d28-4c4e-a9b7-fc239993fa89",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T03:04:53.407527+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:04:53.407527+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4bab072d-5ed9-425e-9982-ea5cd715e2a2",
      "table_name": "PROJECT",
      "record_id": "5361c17f-8581-481a-8903-73df00f7e174",
      "record_pk": {
        "id": "5361c17f-8581-481a-8903-73df00f7e174"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "5361c17f-8581-481a-8903-73df00f7e174",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T03:04:32.320105+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:04:52.84311+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "b4338c7d-6086-4a54-9411-e813ebaf678d",
      "table_name": "PROJECT",
      "record_id": "c2d66fd8-7533-42ff-b315-7d000e93668a",
      "record_pk": {
        "id": "c2d66fd8-7533-42ff-b315-7d000e93668a"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "c2d66fd8-7533-42ff-b315-7d000e93668a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T03:04:32.406113+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:04:52.792661+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "07482ad0-2f1f-46ac-b6bc-f17f7e483194",
      "table_name": "PROJECT",
      "record_id": "c2d66fd8-7533-42ff-b315-7d000e93668a",
      "record_pk": {
        "id": "c2d66fd8-7533-42ff-b315-7d000e93668a"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "c2d66fd8-7533-42ff-b315-7d000e93668a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T03:04:32.406113+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:04:32.406113+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6ad7db29-4bd3-40d4-bc2d-e3b564884769",
      "table_name": "PROJECT",
      "record_id": "5361c17f-8581-481a-8903-73df00f7e174",
      "record_pk": {
        "id": "5361c17f-8581-481a-8903-73df00f7e174"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "5361c17f-8581-481a-8903-73df00f7e174",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T03:04:32.320105+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:04:32.320105+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4061d932-05a5-44a2-96a6-357e3e2d6e4b",
      "table_name": "PROJECT",
      "record_id": "e2baa404-06f4-4e47-93fd-c25985ef9197",
      "record_pk": {
        "id": "e2baa404-06f4-4e47-93fd-c25985ef9197"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "e2baa404-06f4-4e47-93fd-c25985ef9197",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T03:04:10.232585+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:04:31.719435+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "3ef876a8-d2ea-4e87-a5f4-103b45814032",
      "table_name": "PROJECT",
      "record_id": "f7750e5b-5328-45aa-9c23-5204e7b36ef3",
      "record_pk": {
        "id": "f7750e5b-5328-45aa-9c23-5204e7b36ef3"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "f7750e5b-5328-45aa-9c23-5204e7b36ef3",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T03:04:10.304953+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:04:31.612285+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "cd3ef788-06fe-4d01-a290-e33249cb1ccd",
      "table_name": "PROJECT",
      "record_id": "f7750e5b-5328-45aa-9c23-5204e7b36ef3",
      "record_pk": {
        "id": "f7750e5b-5328-45aa-9c23-5204e7b36ef3"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "f7750e5b-5328-45aa-9c23-5204e7b36ef3",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T03:04:10.304953+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:04:10.304953+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d42798c0-50cb-4f5f-8f2d-591ce7668150",
      "table_name": "PROJECT",
      "record_id": "e2baa404-06f4-4e47-93fd-c25985ef9197",
      "record_pk": {
        "id": "e2baa404-06f4-4e47-93fd-c25985ef9197"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "e2baa404-06f4-4e47-93fd-c25985ef9197",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T03:04:10.232585+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T03:04:10.232585+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a1e7471a-0c00-40b4-b9f1-c3d237cd1596",
      "table_name": "PROJECT",
      "record_id": "f55cde18-4a94-4869-8191-dfcf5a6ac469",
      "record_pk": {
        "id": "f55cde18-4a94-4869-8191-dfcf5a6ac469"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "f55cde18-4a94-4869-8191-dfcf5a6ac469",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:55:38.326652+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:56:25.740653+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7b12c17d-b974-4142-a5d0-62e996752446",
      "table_name": "PROJECT",
      "record_id": "f55cde18-4a94-4869-8191-dfcf5a6ac469",
      "record_pk": {
        "id": "f55cde18-4a94-4869-8191-dfcf5a6ac469"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "f55cde18-4a94-4869-8191-dfcf5a6ac469",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:55:38.326652+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:38.326652+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "58c1e6df-7006-4dd0-821a-c098b48e821c",
      "table_name": "PROJECT",
      "record_id": "c9ba863b-a942-427f-aee2-026b6fc14106",
      "record_pk": {
        "id": "c9ba863b-a942-427f-aee2-026b6fc14106"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "c9ba863b-a942-427f-aee2-026b6fc14106",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:55:25.475739+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:37.090614+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "689ed369-cbea-43f1-a64b-a93870196a04",
      "table_name": "PROJECT",
      "record_id": "c9ba863b-a942-427f-aee2-026b6fc14106",
      "record_pk": {
        "id": "c9ba863b-a942-427f-aee2-026b6fc14106"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "c9ba863b-a942-427f-aee2-026b6fc14106",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:55:25.475739+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:25.475739+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "27dace80-e1a3-4942-8153-bd61a67cf148",
      "table_name": "PROJECT",
      "record_id": "8e382c10-f921-4323-b496-495507b4e070",
      "record_pk": {
        "id": "8e382c10-f921-4323-b496-495507b4e070"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "8e382c10-f921-4323-b496-495507b4e070",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:55:13.206676+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:24.733801+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "52d9d0e1-3da7-4739-b5eb-c1147a27b52a",
      "table_name": "PROJECT",
      "record_id": "ea81cd15-81b6-4a17-b1b1-7948f0e919b2",
      "record_pk": {
        "id": "ea81cd15-81b6-4a17-b1b1-7948f0e919b2"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "ea81cd15-81b6-4a17-b1b1-7948f0e919b2",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:55:13.461342+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:24.501956+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7c182c8f-592f-48d9-afe9-fcc7b8d07c2b",
      "table_name": "PROJECT",
      "record_id": "ea81cd15-81b6-4a17-b1b1-7948f0e919b2",
      "record_pk": {
        "id": "ea81cd15-81b6-4a17-b1b1-7948f0e919b2"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "ea81cd15-81b6-4a17-b1b1-7948f0e919b2",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:55:13.461342+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:13.461342+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7ea7ffdf-3463-4c3f-ad17-3aa184db32b4",
      "table_name": "PROJECT",
      "record_id": "8e382c10-f921-4323-b496-495507b4e070",
      "record_pk": {
        "id": "8e382c10-f921-4323-b496-495507b4e070"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "8e382c10-f921-4323-b496-495507b4e070",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:55:13.206676+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:13.206676+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "effcab65-5bf2-4063-93a6-083276c064c6",
      "table_name": "PROJECT",
      "record_id": "3b2f50ae-cc15-4a59-aaba-07cca21fa424",
      "record_pk": {
        "id": "3b2f50ae-cc15-4a59-aaba-07cca21fa424"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "3b2f50ae-cc15-4a59-aaba-07cca21fa424",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:55:00.730396+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:12.442775+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "bbe10a86-4b89-43e8-ac62-8853b17f0bd6",
      "table_name": "PROJECT",
      "record_id": "a08674ba-d6c1-40ce-8957-3fc4aa651272",
      "record_pk": {
        "id": "a08674ba-d6c1-40ce-8957-3fc4aa651272"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "a08674ba-d6c1-40ce-8957-3fc4aa651272",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:55:00.983878+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:12.158429+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0f39a031-aee4-478d-8c41-cea8566badac",
      "table_name": "PROJECT",
      "record_id": "a08674ba-d6c1-40ce-8957-3fc4aa651272",
      "record_pk": {
        "id": "a08674ba-d6c1-40ce-8957-3fc4aa651272"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "a08674ba-d6c1-40ce-8957-3fc4aa651272",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:55:00.983878+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:00.983878+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e4f74569-b5cb-423b-afa3-79fb0d34e349",
      "table_name": "PROJECT",
      "record_id": "3b2f50ae-cc15-4a59-aaba-07cca21fa424",
      "record_pk": {
        "id": "3b2f50ae-cc15-4a59-aaba-07cca21fa424"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "3b2f50ae-cc15-4a59-aaba-07cca21fa424",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:55:00.730396+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:55:00.730396+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "affcf588-7c2c-44d9-aa35-26fc75faed84",
      "table_name": "PROJECT",
      "record_id": "27ed3104-558f-4b08-9c98-78df04deed95",
      "record_pk": {
        "id": "27ed3104-558f-4b08-9c98-78df04deed95"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "27ed3104-558f-4b08-9c98-78df04deed95",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:49:17.806873+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:50:04.188808+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9918bdbc-24bf-4bbf-a7da-75ca9f390293",
      "table_name": "PROJECT",
      "record_id": "27ed3104-558f-4b08-9c98-78df04deed95",
      "record_pk": {
        "id": "27ed3104-558f-4b08-9c98-78df04deed95"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "27ed3104-558f-4b08-9c98-78df04deed95",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:49:17.806873+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:49:17.806873+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "303e7c08-faf6-4a3b-af27-e89815c8f813",
      "table_name": "PROJECT",
      "record_id": "40ce1379-3179-4d34-bb08-15c640e2129f",
      "record_pk": {
        "id": "40ce1379-3179-4d34-bb08-15c640e2129f"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "40ce1379-3179-4d34-bb08-15c640e2129f",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:49:05.349662+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:49:16.558428+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9451b0fd-0dd9-45e4-96de-e16d90fbfba3",
      "table_name": "PROJECT",
      "record_id": "40ce1379-3179-4d34-bb08-15c640e2129f",
      "record_pk": {
        "id": "40ce1379-3179-4d34-bb08-15c640e2129f"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "40ce1379-3179-4d34-bb08-15c640e2129f",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:49:05.349662+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:49:05.349662+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8424d4b1-695b-4271-bdc2-dcaa1d9f2b11",
      "table_name": "PROJECT",
      "record_id": "ac16a01e-29ce-4cfe-9550-ad1472ff6d4b",
      "record_pk": {
        "id": "ac16a01e-29ce-4cfe-9550-ad1472ff6d4b"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "ac16a01e-29ce-4cfe-9550-ad1472ff6d4b",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:48:52.966459+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:49:04.607516+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e7919f08-fc92-4da5-b62f-52e390892234",
      "table_name": "PROJECT",
      "record_id": "a71b8d51-92a7-4fae-ae0a-ad947cb21ddd",
      "record_pk": {
        "id": "a71b8d51-92a7-4fae-ae0a-ad947cb21ddd"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "a71b8d51-92a7-4fae-ae0a-ad947cb21ddd",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:48:53.184184+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:49:04.348222+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "45a02f7a-d034-4b6b-a931-6ae72984327e",
      "table_name": "PROJECT",
      "record_id": "a71b8d51-92a7-4fae-ae0a-ad947cb21ddd",
      "record_pk": {
        "id": "a71b8d51-92a7-4fae-ae0a-ad947cb21ddd"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "a71b8d51-92a7-4fae-ae0a-ad947cb21ddd",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:48:53.184184+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:48:53.184184+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "09cf266f-87a8-4ef6-8bf6-bf340ad891e4",
      "table_name": "PROJECT",
      "record_id": "ac16a01e-29ce-4cfe-9550-ad1472ff6d4b",
      "record_pk": {
        "id": "ac16a01e-29ce-4cfe-9550-ad1472ff6d4b"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "ac16a01e-29ce-4cfe-9550-ad1472ff6d4b",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:48:52.966459+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:48:52.966459+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "189c5ee7-532c-43b4-9349-a5cd1bcab114",
      "table_name": "PROJECT",
      "record_id": "4d1dd884-40c2-4224-8ffa-398c6a56dae6",
      "record_pk": {
        "id": "4d1dd884-40c2-4224-8ffa-398c6a56dae6"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "4d1dd884-40c2-4224-8ffa-398c6a56dae6",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:48:40.813978+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:48:52.220949+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c624c5a5-703f-46c5-886e-0133288298f9",
      "table_name": "PROJECT",
      "record_id": "f3e8f9c2-bef4-4a0a-83e6-86a0c0f5675f",
      "record_pk": {
        "id": "f3e8f9c2-bef4-4a0a-83e6-86a0c0f5675f"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "f3e8f9c2-bef4-4a0a-83e6-86a0c0f5675f",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:48:41.051849+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:48:52.00418+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "63d3bd8e-7e1c-4423-94ca-8aff4a4aa7fa",
      "table_name": "PROJECT",
      "record_id": "f3e8f9c2-bef4-4a0a-83e6-86a0c0f5675f",
      "record_pk": {
        "id": "f3e8f9c2-bef4-4a0a-83e6-86a0c0f5675f"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "f3e8f9c2-bef4-4a0a-83e6-86a0c0f5675f",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:48:41.051849+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:48:41.051849+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a1325b71-657a-49ea-8a59-448e760b7b71",
      "table_name": "PROJECT",
      "record_id": "4d1dd884-40c2-4224-8ffa-398c6a56dae6",
      "record_pk": {
        "id": "4d1dd884-40c2-4224-8ffa-398c6a56dae6"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "4d1dd884-40c2-4224-8ffa-398c6a56dae6",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:48:40.813978+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:48:40.813978+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0bda004f-016f-47ef-b9d3-364418a1c828",
      "table_name": "PROJECT",
      "record_id": "89122de4-9f1f-4f0f-93cd-f7a361066d3a",
      "record_pk": {
        "id": "89122de4-9f1f-4f0f-93cd-f7a361066d3a"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "89122de4-9f1f-4f0f-93cd-f7a361066d3a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:45:27.956933+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:45:28.011358+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "3c196f57-da83-43ca-9db3-4bd04e6d2b74",
      "table_name": "PROJECT",
      "record_id": "89122de4-9f1f-4f0f-93cd-f7a361066d3a",
      "record_pk": {
        "id": "89122de4-9f1f-4f0f-93cd-f7a361066d3a"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "89122de4-9f1f-4f0f-93cd-f7a361066d3a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:45:27.956933+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:45:27.956933+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0ddb2f5d-2e12-42c7-859e-87e63dcb0746",
      "table_name": "PROJECT",
      "record_id": "30feafc4-3c64-42c2-9b96-4dc4861e8fe2",
      "record_pk": {
        "id": "30feafc4-3c64-42c2-9b96-4dc4861e8fe2"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "30feafc4-3c64-42c2-9b96-4dc4861e8fe2",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:45:10.642408+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:45:26.905895+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "695e9af4-3282-4f4e-aaaa-61919d5779a8",
      "table_name": "PROJECT",
      "record_id": "30feafc4-3c64-42c2-9b96-4dc4861e8fe2",
      "record_pk": {
        "id": "30feafc4-3c64-42c2-9b96-4dc4861e8fe2"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "30feafc4-3c64-42c2-9b96-4dc4861e8fe2",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:45:10.642408+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:45:10.642408+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "15c5a728-4176-4e1a-94c9-c1df0750f3da",
      "table_name": "PROJECT",
      "record_id": "25309b5a-f188-482d-902d-94cc9ff370ce",
      "record_pk": {
        "id": "25309b5a-f188-482d-902d-94cc9ff370ce"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "25309b5a-f188-482d-902d-94cc9ff370ce",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:44:55.12409+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:45:10.071426+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "da8b6643-f795-432a-9a95-e9c9d19c6a11",
      "table_name": "PROJECT",
      "record_id": "25e4a6c5-fb99-44eb-a29c-9e98fff36aab",
      "record_pk": {
        "id": "25e4a6c5-fb99-44eb-a29c-9e98fff36aab"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "25e4a6c5-fb99-44eb-a29c-9e98fff36aab",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:44:55.171018+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:45:10.023398+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4cd21872-77d0-4022-bb7d-d4f72fbda440",
      "table_name": "PROJECT",
      "record_id": "25e4a6c5-fb99-44eb-a29c-9e98fff36aab",
      "record_pk": {
        "id": "25e4a6c5-fb99-44eb-a29c-9e98fff36aab"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "25e4a6c5-fb99-44eb-a29c-9e98fff36aab",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:44:55.171018+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:44:55.171018+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4bcf59b3-0408-4f20-82c7-1a8cc21f7da4",
      "table_name": "PROJECT",
      "record_id": "25309b5a-f188-482d-902d-94cc9ff370ce",
      "record_pk": {
        "id": "25309b5a-f188-482d-902d-94cc9ff370ce"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "25309b5a-f188-482d-902d-94cc9ff370ce",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:44:55.12409+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:44:55.12409+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7dc1cfb4-a6dc-4973-95c1-ace828bd8cb1",
      "table_name": "PROJECT",
      "record_id": "9f55e9da-8178-437f-843c-648cfadd257b",
      "record_pk": {
        "id": "9f55e9da-8178-437f-843c-648cfadd257b"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "9f55e9da-8178-437f-843c-648cfadd257b",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:44:35.248652+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:44:54.570779+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "2e4c61fa-b9ba-414a-868f-89dd7e2f0d07",
      "table_name": "PROJECT",
      "record_id": "d0cbc2a9-2615-47ae-8660-83e7c0f7f337",
      "record_pk": {
        "id": "d0cbc2a9-2615-47ae-8660-83e7c0f7f337"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "d0cbc2a9-2615-47ae-8660-83e7c0f7f337",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:44:35.296616+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:44:54.529036+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "b143ce16-012b-47b7-abc9-6026a5a25593",
      "table_name": "PROJECT",
      "record_id": "d0cbc2a9-2615-47ae-8660-83e7c0f7f337",
      "record_pk": {
        "id": "d0cbc2a9-2615-47ae-8660-83e7c0f7f337"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "d0cbc2a9-2615-47ae-8660-83e7c0f7f337",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:44:35.296616+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:44:35.296616+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "52ec4df5-fcae-429a-ac3d-c6ff07447376",
      "table_name": "PROJECT",
      "record_id": "9f55e9da-8178-437f-843c-648cfadd257b",
      "record_pk": {
        "id": "9f55e9da-8178-437f-843c-648cfadd257b"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "9f55e9da-8178-437f-843c-648cfadd257b",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:44:35.248652+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:44:35.248652+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "250a1fc8-b82e-4685-a300-9ff8cb7278f3",
      "table_name": "PROJECT",
      "record_id": "2704a730-f5e8-4648-9f28-f9fbe989c5ca",
      "record_pk": {
        "id": "2704a730-f5e8-4648-9f28-f9fbe989c5ca"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "2704a730-f5e8-4648-9f28-f9fbe989c5ca",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:43:44.574733+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:43:45.968417+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "1913c465-c8e2-4172-80cf-3d0c3928a8ab",
      "table_name": "PROJECT",
      "record_id": "2704a730-f5e8-4648-9f28-f9fbe989c5ca",
      "record_pk": {
        "id": "2704a730-f5e8-4648-9f28-f9fbe989c5ca"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "2704a730-f5e8-4648-9f28-f9fbe989c5ca",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:43:44.574733+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:43:44.574733+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "2c15bf6b-f4e6-4eef-bee1-4509ad74b43c",
      "table_name": "PROJECT",
      "record_id": "5ab32946-4823-43b5-b2d1-816e67c604fb",
      "record_pk": {
        "id": "5ab32946-4823-43b5-b2d1-816e67c604fb"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "5ab32946-4823-43b5-b2d1-816e67c604fb",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:43:17.790758+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:43:43.492415+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "75521ec7-4265-462a-8216-842ec57448a2",
      "table_name": "PROJECT",
      "record_id": "5ab32946-4823-43b5-b2d1-816e67c604fb",
      "record_pk": {
        "id": "5ab32946-4823-43b5-b2d1-816e67c604fb"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "5ab32946-4823-43b5-b2d1-816e67c604fb",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:43:17.790758+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:43:17.790758+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f642e8ac-a463-403e-896b-86a913b63885",
      "table_name": "PROJECT",
      "record_id": "23842333-4bef-45a4-b975-800c7f466d23",
      "record_pk": {
        "id": "23842333-4bef-45a4-b975-800c7f466d23"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "23842333-4bef-45a4-b975-800c7f466d23",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:42:51.341865+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:43:17.210545+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "adc7c399-c761-4ed5-843a-dba976fd556d",
      "table_name": "PROJECT",
      "record_id": "5ffe6b6b-ca00-498e-91bd-564c56f534d2",
      "record_pk": {
        "id": "5ffe6b6b-ca00-498e-91bd-564c56f534d2"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "5ffe6b6b-ca00-498e-91bd-564c56f534d2",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:42:51.437587+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:43:17.147583+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c839daa3-a9e1-4f71-b088-149997a3a6c3",
      "table_name": "PROJECT",
      "record_id": "5ffe6b6b-ca00-498e-91bd-564c56f534d2",
      "record_pk": {
        "id": "5ffe6b6b-ca00-498e-91bd-564c56f534d2"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "5ffe6b6b-ca00-498e-91bd-564c56f534d2",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:42:51.437587+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:42:51.437587+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8ac711b8-85ce-4d99-bea1-bfbaaf71c124",
      "table_name": "PROJECT",
      "record_id": "23842333-4bef-45a4-b975-800c7f466d23",
      "record_pk": {
        "id": "23842333-4bef-45a4-b975-800c7f466d23"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "23842333-4bef-45a4-b975-800c7f466d23",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:42:51.341865+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:42:51.341865+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "06d80a6a-79ae-4d89-bd69-43f961d2b0af",
      "table_name": "PROJECT",
      "record_id": "76cf52cd-7583-463c-ba45-39100978ddb1",
      "record_pk": {
        "id": "76cf52cd-7583-463c-ba45-39100978ddb1"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "76cf52cd-7583-463c-ba45-39100978ddb1",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:42:24.717879+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:42:50.771086+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6d10b5bb-8b0f-40d6-b149-d010af31dde5",
      "table_name": "PROJECT",
      "record_id": "4dbecaaa-6e87-4a95-b7f1-81532e648ff8",
      "record_pk": {
        "id": "4dbecaaa-6e87-4a95-b7f1-81532e648ff8"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "4dbecaaa-6e87-4a95-b7f1-81532e648ff8",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:42:24.979302+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:42:50.682913+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9cb08e95-934d-421b-8339-b530508e7204",
      "table_name": "PROJECT",
      "record_id": "4dbecaaa-6e87-4a95-b7f1-81532e648ff8",
      "record_pk": {
        "id": "4dbecaaa-6e87-4a95-b7f1-81532e648ff8"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "4dbecaaa-6e87-4a95-b7f1-81532e648ff8",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:42:24.979302+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:42:24.979302+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c65fcd54-fa92-43d7-b741-03e722e8d5bf",
      "table_name": "PROJECT",
      "record_id": "76cf52cd-7583-463c-ba45-39100978ddb1",
      "record_pk": {
        "id": "76cf52cd-7583-463c-ba45-39100978ddb1"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "76cf52cd-7583-463c-ba45-39100978ddb1",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:42:24.717879+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:42:24.717879+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "910a78fa-75ed-42db-9b89-115e77479114",
      "table_name": "PROJECT",
      "record_id": "addb49bd-fdcb-43e1-9564-b2a25ae998bb",
      "record_pk": {
        "id": "addb49bd-fdcb-43e1-9564-b2a25ae998bb"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "addb49bd-fdcb-43e1-9564-b2a25ae998bb",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:35:55.13135+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:35:55.13135+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8ec0348b-b19d-46e1-aaa9-a6d624b0c198",
      "table_name": "PROJECT",
      "record_id": "dbcf21eb-1cbf-4d45-90cf-49a180344c8e",
      "record_pk": {
        "id": "dbcf21eb-1cbf-4d45-90cf-49a180344c8e"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "dbcf21eb-1cbf-4d45-90cf-49a180344c8e",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:35:28.750856+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:35:54.57648+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "99c4a39e-48b6-4979-ad7b-d8231a9914a0",
      "table_name": "PROJECT",
      "record_id": "486cdeca-5657-4056-a37b-12fff02d9dee",
      "record_pk": {
        "id": "486cdeca-5657-4056-a37b-12fff02d9dee"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "486cdeca-5657-4056-a37b-12fff02d9dee",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:35:28.815495+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:35:54.522498+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c979bf29-8155-461f-b271-27097c8d89b9",
      "table_name": "PROJECT",
      "record_id": "486cdeca-5657-4056-a37b-12fff02d9dee",
      "record_pk": {
        "id": "486cdeca-5657-4056-a37b-12fff02d9dee"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "486cdeca-5657-4056-a37b-12fff02d9dee",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:35:28.815495+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:35:28.815495+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "36867a1a-a491-48ed-b51d-9288614607bb",
      "table_name": "PROJECT",
      "record_id": "dbcf21eb-1cbf-4d45-90cf-49a180344c8e",
      "record_pk": {
        "id": "dbcf21eb-1cbf-4d45-90cf-49a180344c8e"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "dbcf21eb-1cbf-4d45-90cf-49a180344c8e",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:35:28.750856+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:35:28.750856+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4a99443f-3372-4768-afb7-5faf89d23a57",
      "table_name": "PROJECT",
      "record_id": "568fd34a-40f9-46e5-a5f6-38ea9ee34a31",
      "record_pk": {
        "id": "568fd34a-40f9-46e5-a5f6-38ea9ee34a31"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "568fd34a-40f9-46e5-a5f6-38ea9ee34a31",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:35:02.106267+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:35:28.149302+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4c8b6db8-d390-4c4d-96ec-fdac911e6191",
      "table_name": "PROJECT",
      "record_id": "f58d44ae-c19d-406c-8e35-8854fd8521a5",
      "record_pk": {
        "id": "f58d44ae-c19d-406c-8e35-8854fd8521a5"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "f58d44ae-c19d-406c-8e35-8854fd8521a5",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:35:02.313798+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:35:28.043887+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "14e2df8a-a918-40b3-8dd4-18068838c9a0",
      "table_name": "PROJECT",
      "record_id": "f58d44ae-c19d-406c-8e35-8854fd8521a5",
      "record_pk": {
        "id": "f58d44ae-c19d-406c-8e35-8854fd8521a5"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "f58d44ae-c19d-406c-8e35-8854fd8521a5",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:35:02.313798+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:35:02.313798+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "806883bd-6c04-4858-b395-786e4cebaef3",
      "table_name": "PROJECT",
      "record_id": "568fd34a-40f9-46e5-a5f6-38ea9ee34a31",
      "record_pk": {
        "id": "568fd34a-40f9-46e5-a5f6-38ea9ee34a31"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "568fd34a-40f9-46e5-a5f6-38ea9ee34a31",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:35:02.106267+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:35:02.106267+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ecb4a09e-c328-431e-855b-f09e2630702d",
      "table_name": "PROJECT",
      "record_id": "9ba5eccb-9c4a-464c-be4b-029b2a1ae368",
      "record_pk": {
        "id": "9ba5eccb-9c4a-464c-be4b-029b2a1ae368"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "9ba5eccb-9c4a-464c-be4b-029b2a1ae368",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:28:25.494416+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:28:31.503258+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4c8a0da3-83a0-4ce7-a294-0bdf8c2b93f5",
      "table_name": "PROJECT",
      "record_id": "9ba5eccb-9c4a-464c-be4b-029b2a1ae368",
      "record_pk": {
        "id": "9ba5eccb-9c4a-464c-be4b-029b2a1ae368"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "9ba5eccb-9c4a-464c-be4b-029b2a1ae368",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:28:25.494416+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:28:25.494416+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c55e8708-618f-4394-a2dc-576ecdad6aa3",
      "table_name": "PROJECT",
      "record_id": "3b3c81dc-d4e6-42f6-a1b2-6f8dd9e1b767",
      "record_pk": {
        "id": "3b3c81dc-d4e6-42f6-a1b2-6f8dd9e1b767"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "3b3c81dc-d4e6-42f6-a1b2-6f8dd9e1b767",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:28:12.33219+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:28:24.406174+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "70a256ce-afc1-45b7-961f-709b86b5ce80",
      "table_name": "PROJECT",
      "record_id": "3b3c81dc-d4e6-42f6-a1b2-6f8dd9e1b767",
      "record_pk": {
        "id": "3b3c81dc-d4e6-42f6-a1b2-6f8dd9e1b767"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "3b3c81dc-d4e6-42f6-a1b2-6f8dd9e1b767",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:28:12.33219+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:28:12.33219+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7d326cf1-81bb-4e59-ac60-cd7e218a957d",
      "table_name": "PROJECT",
      "record_id": "9b6104fe-98e1-465e-a5ef-6f4dd97ae0b3",
      "record_pk": {
        "id": "9b6104fe-98e1-465e-a5ef-6f4dd97ae0b3"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "9b6104fe-98e1-465e-a5ef-6f4dd97ae0b3",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:27:59.600852+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:28:11.769773+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e9b8697e-d04b-464a-b9af-5d77d322fe48",
      "table_name": "PROJECT",
      "record_id": "3e0f2799-da26-489f-900e-460b6fa93086",
      "record_pk": {
        "id": "3e0f2799-da26-489f-900e-460b6fa93086"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "3e0f2799-da26-489f-900e-460b6fa93086",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:27:59.669474+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:28:11.724428+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "bd3d78b6-54a8-4751-a33e-ff3b6e311b58",
      "table_name": "PROJECT",
      "record_id": "3e0f2799-da26-489f-900e-460b6fa93086",
      "record_pk": {
        "id": "3e0f2799-da26-489f-900e-460b6fa93086"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "3e0f2799-da26-489f-900e-460b6fa93086",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:27:59.669474+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:59.669474+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7ace7fac-3f70-489f-8e16-bf7620e48d6f",
      "table_name": "PROJECT",
      "record_id": "9b6104fe-98e1-465e-a5ef-6f4dd97ae0b3",
      "record_pk": {
        "id": "9b6104fe-98e1-465e-a5ef-6f4dd97ae0b3"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "9b6104fe-98e1-465e-a5ef-6f4dd97ae0b3",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:27:59.600852+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:59.600852+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "cd34a7a2-a6eb-455d-b5ea-1cd8c75581a6",
      "table_name": "PROJECT",
      "record_id": "551c9f0b-11b4-40ff-905e-a7c21d8f6300",
      "record_pk": {
        "id": "551c9f0b-11b4-40ff-905e-a7c21d8f6300"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "551c9f0b-11b4-40ff-905e-a7c21d8f6300",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:27:46.834301+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:59.033117+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8b6e58d5-2038-480f-bf92-f337d34f5bff",
      "table_name": "PROJECT",
      "record_id": "fd1f0700-9072-40bd-a41c-c2d81a33bd92",
      "record_pk": {
        "id": "fd1f0700-9072-40bd-a41c-c2d81a33bd92"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "fd1f0700-9072-40bd-a41c-c2d81a33bd92",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:27:46.885508+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:58.96886+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ab7149ec-97bd-4d55-af74-ef95df339a5e",
      "table_name": "PROJECT",
      "record_id": "74d823cf-869e-4afc-b929-0391ed775c46",
      "record_pk": {
        "id": "74d823cf-869e-4afc-b929-0391ed775c46"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "74d823cf-869e-4afc-b929-0391ed775c46",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:27:24.177527+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:53.352076+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "de713d6c-0ea6-4e80-b6d4-31ba6a791410",
      "table_name": "PROJECT",
      "record_id": "fd1f0700-9072-40bd-a41c-c2d81a33bd92",
      "record_pk": {
        "id": "fd1f0700-9072-40bd-a41c-c2d81a33bd92"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "fd1f0700-9072-40bd-a41c-c2d81a33bd92",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:27:46.885508+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:46.885508+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e3626965-ebb0-4767-862f-56213a75670f",
      "table_name": "PROJECT",
      "record_id": "551c9f0b-11b4-40ff-905e-a7c21d8f6300",
      "record_pk": {
        "id": "551c9f0b-11b4-40ff-905e-a7c21d8f6300"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "551c9f0b-11b4-40ff-905e-a7c21d8f6300",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:27:46.834301+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:46.834301+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d335bebb-d7d7-4597-a23f-52a4a641b853",
      "table_name": "PROJECT",
      "record_id": "74d823cf-869e-4afc-b929-0391ed775c46",
      "record_pk": {
        "id": "74d823cf-869e-4afc-b929-0391ed775c46"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "74d823cf-869e-4afc-b929-0391ed775c46",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:27:24.177527+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:24.177527+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6515168a-4d79-4413-9c0e-63d80a308fe7",
      "table_name": "PROJECT",
      "record_id": "ffae87cf-fb08-43fd-9a73-43cf818e9218",
      "record_pk": {
        "id": "ffae87cf-fb08-43fd-9a73-43cf818e9218"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "ffae87cf-fb08-43fd-9a73-43cf818e9218",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:27:10.84703+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:22.868566+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0e36f001-6682-4ba5-81ee-b5471f78511e",
      "table_name": "PROJECT",
      "record_id": "ffae87cf-fb08-43fd-9a73-43cf818e9218",
      "record_pk": {
        "id": "ffae87cf-fb08-43fd-9a73-43cf818e9218"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "ffae87cf-fb08-43fd-9a73-43cf818e9218",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:27:10.84703+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:10.84703+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "99fc7c33-3f2d-4bb5-9aa9-3c3d1eb36a4d",
      "table_name": "PROJECT",
      "record_id": "72b1bc90-3408-4881-a8b9-2ab72f827c04",
      "record_pk": {
        "id": "72b1bc90-3408-4881-a8b9-2ab72f827c04"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "72b1bc90-3408-4881-a8b9-2ab72f827c04",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:26:58.288426+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:10.060167+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "81cddb1f-ef99-447f-bdd3-722571311451",
      "table_name": "PROJECT",
      "record_id": "7c045b03-2793-49e5-bcc1-5be30320e914",
      "record_pk": {
        "id": "7c045b03-2793-49e5-bcc1-5be30320e914"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "7c045b03-2793-49e5-bcc1-5be30320e914",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:26:58.557923+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:27:09.78885+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "3f72d0f3-c26d-40ff-82f4-bc2372b5cfc5",
      "table_name": "PROJECT",
      "record_id": "7c045b03-2793-49e5-bcc1-5be30320e914",
      "record_pk": {
        "id": "7c045b03-2793-49e5-bcc1-5be30320e914"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "7c045b03-2793-49e5-bcc1-5be30320e914",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:26:58.557923+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:26:58.557923+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4cb3c842-38b9-4382-be5b-023b64bc3fdd",
      "table_name": "PROJECT",
      "record_id": "72b1bc90-3408-4881-a8b9-2ab72f827c04",
      "record_pk": {
        "id": "72b1bc90-3408-4881-a8b9-2ab72f827c04"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "72b1bc90-3408-4881-a8b9-2ab72f827c04",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:26:58.288426+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:26:58.288426+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "63e2b56f-14f1-4f1a-9004-23ecfc39d4aa",
      "table_name": "PROJECT",
      "record_id": "1ae46053-34b9-460d-a352-2e56098872ef",
      "record_pk": {
        "id": "1ae46053-34b9-460d-a352-2e56098872ef"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "1ae46053-34b9-460d-a352-2e56098872ef",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:26:45.843096+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:26:57.489118+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6911c923-26c2-47a7-9c6b-76e37dcf3d5e",
      "table_name": "PROJECT",
      "record_id": "bef1024a-41f1-44e0-84ca-39fcf9b6653d",
      "record_pk": {
        "id": "bef1024a-41f1-44e0-84ca-39fcf9b6653d"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "bef1024a-41f1-44e0-84ca-39fcf9b6653d",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:26:46.15607+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:26:57.188785+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a90ba4b6-72f4-4fc8-b684-c9d22ff47faf",
      "table_name": "PROJECT",
      "record_id": "bef1024a-41f1-44e0-84ca-39fcf9b6653d",
      "record_pk": {
        "id": "bef1024a-41f1-44e0-84ca-39fcf9b6653d"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "bef1024a-41f1-44e0-84ca-39fcf9b6653d",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:26:46.15607+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:26:46.15607+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "865d59bf-0b84-441f-8114-b2d35a1346dc",
      "table_name": "PROJECT",
      "record_id": "1ae46053-34b9-460d-a352-2e56098872ef",
      "record_pk": {
        "id": "1ae46053-34b9-460d-a352-2e56098872ef"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "1ae46053-34b9-460d-a352-2e56098872ef",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:26:45.843096+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:26:45.843096+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ffc30846-5471-4e46-9154-2159443a9eb2",
      "table_name": "PROJECT",
      "record_id": "918b6624-73a6-453b-ad51-3bb1e889041e",
      "record_pk": {
        "id": "918b6624-73a6-453b-ad51-3bb1e889041e"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "918b6624-73a6-453b-ad51-3bb1e889041e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:15:04.075113+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:15:20.113818+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "473de7cd-b5b1-412c-8940-da68e694ea3d",
      "table_name": "PROJECT",
      "record_id": "918b6624-73a6-453b-ad51-3bb1e889041e",
      "record_pk": {
        "id": "918b6624-73a6-453b-ad51-3bb1e889041e"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "918b6624-73a6-453b-ad51-3bb1e889041e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:15:04.075113+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:15:04.075113+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4054371b-fc77-4089-a8d3-87c78f2feff1",
      "table_name": "PROJECT",
      "record_id": "bf9eab62-d9b4-4479-a544-d6359de04ad5",
      "record_pk": {
        "id": "bf9eab62-d9b4-4479-a544-d6359de04ad5"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "bf9eab62-d9b4-4479-a544-d6359de04ad5",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:14:50.669789+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:15:02.781952+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "817931d8-c733-404e-bb03-2018fd9c199a",
      "table_name": "PROJECT",
      "record_id": "bf9eab62-d9b4-4479-a544-d6359de04ad5",
      "record_pk": {
        "id": "bf9eab62-d9b4-4479-a544-d6359de04ad5"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "bf9eab62-d9b4-4479-a544-d6359de04ad5",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:14:50.669789+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:14:50.669789+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "942226f1-12e0-431a-a7ab-d3144bffdd30",
      "table_name": "PROJECT",
      "record_id": "b65b372b-24ec-4368-a262-2a1ecf8f747e",
      "record_pk": {
        "id": "b65b372b-24ec-4368-a262-2a1ecf8f747e"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "b65b372b-24ec-4368-a262-2a1ecf8f747e",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:14:37.435428+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:14:49.858739+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "83316b7d-084e-4a4a-ad50-fa0e16c8cbbf",
      "table_name": "PROJECT",
      "record_id": "281467dd-7b5b-4089-9986-61bd9ac22a01",
      "record_pk": {
        "id": "281467dd-7b5b-4089-9986-61bd9ac22a01"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "281467dd-7b5b-4089-9986-61bd9ac22a01",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:14:37.727069+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:14:49.03141+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "808ba7a3-e3c1-4b60-b4bc-d046e9e8e448",
      "table_name": "PROJECT",
      "record_id": "281467dd-7b5b-4089-9986-61bd9ac22a01",
      "record_pk": {
        "id": "281467dd-7b5b-4089-9986-61bd9ac22a01"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "281467dd-7b5b-4089-9986-61bd9ac22a01",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:14:37.727069+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:14:37.727069+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "2f9bdb0c-2962-45c1-88e7-1b5ec297ed85",
      "table_name": "PROJECT",
      "record_id": "b65b372b-24ec-4368-a262-2a1ecf8f747e",
      "record_pk": {
        "id": "b65b372b-24ec-4368-a262-2a1ecf8f747e"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "b65b372b-24ec-4368-a262-2a1ecf8f747e",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:14:37.435428+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:14:37.435428+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6f8e30a0-efa9-4f73-9cb8-ed3b1271e937",
      "table_name": "PROJECT",
      "record_id": "e5f4e344-8519-45ef-8c29-b9cd40e8c1d1",
      "record_pk": {
        "id": "e5f4e344-8519-45ef-8c29-b9cd40e8c1d1"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "e5f4e344-8519-45ef-8c29-b9cd40e8c1d1",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:14:24.919369+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:14:36.634796+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "5735ed1e-445a-4f9c-9e73-7c294bc0064c",
      "table_name": "PROJECT",
      "record_id": "aaffa39c-5ce2-4eb3-8bf9-079a7da0dbd4",
      "record_pk": {
        "id": "aaffa39c-5ce2-4eb3-8bf9-079a7da0dbd4"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "aaffa39c-5ce2-4eb3-8bf9-079a7da0dbd4",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:14:25.304445+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:14:36.330523+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d9fa49ee-5ca8-4780-b749-c5c41908ba9b",
      "table_name": "PROJECT",
      "record_id": "aaffa39c-5ce2-4eb3-8bf9-079a7da0dbd4",
      "record_pk": {
        "id": "aaffa39c-5ce2-4eb3-8bf9-079a7da0dbd4"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "aaffa39c-5ce2-4eb3-8bf9-079a7da0dbd4",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:14:25.304445+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:14:25.304445+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "b1f8a32a-d94a-47f8-a645-539f515b5164",
      "table_name": "PROJECT",
      "record_id": "e5f4e344-8519-45ef-8c29-b9cd40e8c1d1",
      "record_pk": {
        "id": "e5f4e344-8519-45ef-8c29-b9cd40e8c1d1"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "e5f4e344-8519-45ef-8c29-b9cd40e8c1d1",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:14:24.919369+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:14:24.919369+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "11f78eb0-a410-442f-be51-9db7e7da3f9d",
      "table_name": "PROJECT",
      "record_id": "78d5d9d6-8508-4a61-b726-5dc84251c22d",
      "record_pk": {
        "id": "78d5d9d6-8508-4a61-b726-5dc84251c22d"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "78d5d9d6-8508-4a61-b726-5dc84251c22d",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:10:44.54176+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:11:20.816953+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ac483089-6ee5-43f2-adbb-9ac68d9c9314",
      "table_name": "PROJECT",
      "record_id": "78d5d9d6-8508-4a61-b726-5dc84251c22d",
      "record_pk": {
        "id": "78d5d9d6-8508-4a61-b726-5dc84251c22d"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "78d5d9d6-8508-4a61-b726-5dc84251c22d",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:10:44.54176+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:44.54176+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7274565a-5914-40f0-a56d-c4039ae73e7e",
      "table_name": "PROJECT",
      "record_id": "0d24ba0e-13bd-4a43-a27c-d45f2e3f5631",
      "record_pk": {
        "id": "0d24ba0e-13bd-4a43-a27c-d45f2e3f5631"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "0d24ba0e-13bd-4a43-a27c-d45f2e3f5631",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:10:31.032089+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:43.282792+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "42b7447b-df37-4768-b413-b7cb52fef726",
      "table_name": "PROJECT",
      "record_id": "0d24ba0e-13bd-4a43-a27c-d45f2e3f5631",
      "record_pk": {
        "id": "0d24ba0e-13bd-4a43-a27c-d45f2e3f5631"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "0d24ba0e-13bd-4a43-a27c-d45f2e3f5631",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:10:31.032089+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:31.032089+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "927b5c77-dd21-4fed-9ea2-447842202118",
      "table_name": "PROJECT",
      "record_id": "2efd0095-805d-4bf9-a482-6c25cac11d84",
      "record_pk": {
        "id": "2efd0095-805d-4bf9-a482-6c25cac11d84"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "2efd0095-805d-4bf9-a482-6c25cac11d84",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:10:18.624672+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:30.17121+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "bded12ab-c74f-4f35-87e5-5687b84fbf59",
      "table_name": "PROJECT",
      "record_id": "44c263a0-6ef1-4102-8d8c-0965bc202771",
      "record_pk": {
        "id": "44c263a0-6ef1-4102-8d8c-0965bc202771"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "44c263a0-6ef1-4102-8d8c-0965bc202771",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:10:18.85717+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:29.900352+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9df929ed-554c-468f-ad9c-de9e24395a23",
      "table_name": "PROJECT",
      "record_id": "44c263a0-6ef1-4102-8d8c-0965bc202771",
      "record_pk": {
        "id": "44c263a0-6ef1-4102-8d8c-0965bc202771"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "44c263a0-6ef1-4102-8d8c-0965bc202771",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:10:18.85717+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:18.85717+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "5cba3f68-add5-423c-aa6f-8b3719e0555c",
      "table_name": "PROJECT",
      "record_id": "2efd0095-805d-4bf9-a482-6c25cac11d84",
      "record_pk": {
        "id": "2efd0095-805d-4bf9-a482-6c25cac11d84"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "2efd0095-805d-4bf9-a482-6c25cac11d84",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:10:18.624672+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:18.624672+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "65ca076a-10a0-42a0-9cd4-d8e5211ff41a",
      "table_name": "PROJECT",
      "record_id": "8ea2b12d-8230-412c-993f-ba8d0154d534",
      "record_pk": {
        "id": "8ea2b12d-8230-412c-993f-ba8d0154d534"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "8ea2b12d-8230-412c-993f-ba8d0154d534",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:10:06.167018+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:17.862567+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e6613d52-c190-404d-8ce3-c6be6bc3c5cf",
      "table_name": "PROJECT",
      "record_id": "e5045dea-0d49-4fb6-94a1-aa735c994eee",
      "record_pk": {
        "id": "e5045dea-0d49-4fb6-94a1-aa735c994eee"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "e5045dea-0d49-4fb6-94a1-aa735c994eee",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:10:06.751097+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:17.489674+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "02fccc6a-5c95-4141-8546-952203527787",
      "table_name": "PROJECT",
      "record_id": "e5045dea-0d49-4fb6-94a1-aa735c994eee",
      "record_pk": {
        "id": "e5045dea-0d49-4fb6-94a1-aa735c994eee"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "e5045dea-0d49-4fb6-94a1-aa735c994eee",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:10:06.751097+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:06.751097+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "3c4d45c6-5f6f-43ef-bd64-1f78518dffb0",
      "table_name": "PROJECT",
      "record_id": "8ea2b12d-8230-412c-993f-ba8d0154d534",
      "record_pk": {
        "id": "8ea2b12d-8230-412c-993f-ba8d0154d534"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "8ea2b12d-8230-412c-993f-ba8d0154d534",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:10:06.167018+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:10:06.167018+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "dc974b13-f79d-42ef-93b0-bf2887ed860e",
      "table_name": "PROJECT",
      "record_id": "3f654319-50d3-47a5-ae8e-0c04bbe62af8",
      "record_pk": {
        "id": "3f654319-50d3-47a5-ae8e-0c04bbe62af8"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "3f654319-50d3-47a5-ae8e-0c04bbe62af8",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:02:52.426195+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:52.493708+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "1b841762-a15b-4e93-b1fd-3c2f3716033d",
      "table_name": "PROJECT",
      "record_id": "3f654319-50d3-47a5-ae8e-0c04bbe62af8",
      "record_pk": {
        "id": "3f654319-50d3-47a5-ae8e-0c04bbe62af8"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "3f654319-50d3-47a5-ae8e-0c04bbe62af8",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:02:52.426195+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:52.426195+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "2aa0b363-c902-4ba8-a020-f024eb639ef2",
      "table_name": "PROJECT",
      "record_id": "c49da4ca-e02b-4c87-b3c8-6cb0415282a5",
      "record_pk": {
        "id": "c49da4ca-e02b-4c87-b3c8-6cb0415282a5"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "c49da4ca-e02b-4c87-b3c8-6cb0415282a5",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:02:40.189204+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:51.37612+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "70da3d06-7ed8-4237-9717-d4549a92e2bf",
      "table_name": "PROJECT",
      "record_id": "c49da4ca-e02b-4c87-b3c8-6cb0415282a5",
      "record_pk": {
        "id": "c49da4ca-e02b-4c87-b3c8-6cb0415282a5"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "c49da4ca-e02b-4c87-b3c8-6cb0415282a5",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:02:40.189204+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:40.189204+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d73622cc-b024-41aa-9fb0-e6755949c638",
      "table_name": "PROJECT",
      "record_id": "362afa2c-1ad6-46bc-9ed8-d14dfefddf4f",
      "record_pk": {
        "id": "362afa2c-1ad6-46bc-9ed8-d14dfefddf4f"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "362afa2c-1ad6-46bc-9ed8-d14dfefddf4f",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:02:30.247983+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:39.641468+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a2796ea4-3f8f-4f5c-b1a7-44ea596fe6d2",
      "table_name": "PROJECT",
      "record_id": "57bd3bdb-0770-45f5-87f7-80dd1834a01e",
      "record_pk": {
        "id": "57bd3bdb-0770-45f5-87f7-80dd1834a01e"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "57bd3bdb-0770-45f5-87f7-80dd1834a01e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:02:30.28464+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:39.606018+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "583e14e6-7429-4083-a292-ff71999137fc",
      "table_name": "PROJECT",
      "record_id": "57bd3bdb-0770-45f5-87f7-80dd1834a01e",
      "record_pk": {
        "id": "57bd3bdb-0770-45f5-87f7-80dd1834a01e"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "57bd3bdb-0770-45f5-87f7-80dd1834a01e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T02:02:30.28464+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:30.28464+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e3214f23-bad2-43a7-845e-232660e6b5fc",
      "table_name": "PROJECT",
      "record_id": "362afa2c-1ad6-46bc-9ed8-d14dfefddf4f",
      "record_pk": {
        "id": "362afa2c-1ad6-46bc-9ed8-d14dfefddf4f"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "362afa2c-1ad6-46bc-9ed8-d14dfefddf4f",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T02:02:30.247983+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:30.247983+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c5ba3c21-0821-4c01-abc6-457013990830",
      "table_name": "PROJECT",
      "record_id": "03acf5a8-7e68-4364-91ce-47a9260514b0",
      "record_pk": {
        "id": "03acf5a8-7e68-4364-91ce-47a9260514b0"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "03acf5a8-7e68-4364-91ce-47a9260514b0",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:02:17.576537+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:29.700165+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "20b6de3e-fea5-4e7b-a611-c70394f6ca9d",
      "table_name": "PROJECT",
      "record_id": "337987ff-6af0-4800-8e2f-a4e0ab6c7048",
      "record_pk": {
        "id": "337987ff-6af0-4800-8e2f-a4e0ab6c7048"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "337987ff-6af0-4800-8e2f-a4e0ab6c7048",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:02:17.625608+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:29.664525+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "bbdeb02d-721c-4118-a7fe-6f52e28de78b",
      "table_name": "PROJECT",
      "record_id": "337987ff-6af0-4800-8e2f-a4e0ab6c7048",
      "record_pk": {
        "id": "337987ff-6af0-4800-8e2f-a4e0ab6c7048"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "337987ff-6af0-4800-8e2f-a4e0ab6c7048",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T02:02:17.625608+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:17.625608+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "1cfe3666-1888-4fe8-9f11-6aa15272cc64",
      "table_name": "PROJECT",
      "record_id": "03acf5a8-7e68-4364-91ce-47a9260514b0",
      "record_pk": {
        "id": "03acf5a8-7e68-4364-91ce-47a9260514b0"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "03acf5a8-7e68-4364-91ce-47a9260514b0",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T02:02:17.576537+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:02:17.576537+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ce018879-77df-4d4c-8607-1ead176c96c5",
      "table_name": "PROJECT",
      "record_id": "7301c314-9484-4d00-9091-fed4c199d173",
      "record_pk": {
        "id": "7301c314-9484-4d00-9091-fed4c199d173"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "7301c314-9484-4d00-9091-fed4c199d173",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:00:17.271496+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:00:32.5094+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a50b0ce5-eecd-49fe-95bf-f1e202fec339",
      "table_name": "PROJECT",
      "record_id": "7301c314-9484-4d00-9091-fed4c199d173",
      "record_pk": {
        "id": "7301c314-9484-4d00-9091-fed4c199d173"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "7301c314-9484-4d00-9091-fed4c199d173",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T02:00:17.271496+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:00:17.271496+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7468f870-71db-4a48-9179-e76243cbb30e",
      "table_name": "PROJECT",
      "record_id": "0849606a-1130-4199-9a3b-629662f27107",
      "record_pk": {
        "id": "0849606a-1130-4199-9a3b-629662f27107"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "0849606a-1130-4199-9a3b-629662f27107",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:00:04.343614+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:00:16.030423+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "bfc81657-9b39-4610-894b-c089b6020c2e",
      "table_name": "PROJECT",
      "record_id": "0849606a-1130-4199-9a3b-629662f27107",
      "record_pk": {
        "id": "0849606a-1130-4199-9a3b-629662f27107"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "0849606a-1130-4199-9a3b-629662f27107",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T02:00:04.343614+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:00:04.343614+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a3382f0d-07f6-42b6-bbb7-4f29d0f7a8e9",
      "table_name": "PROJECT",
      "record_id": "ab6ccada-dcb2-4554-8748-2a95fb69bd78",
      "record_pk": {
        "id": "ab6ccada-dcb2-4554-8748-2a95fb69bd78"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "ab6ccada-dcb2-4554-8748-2a95fb69bd78",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T01:59:52.096438+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:00:03.595887+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c4abface-b346-48a9-bc52-5a9684d2a700",
      "table_name": "PROJECT",
      "record_id": "90aeb75e-807f-4682-825e-f84ab4ab8315",
      "record_pk": {
        "id": "90aeb75e-807f-4682-825e-f84ab4ab8315"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "90aeb75e-807f-4682-825e-f84ab4ab8315",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T01:59:52.329558+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T02:00:03.349533+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "11a9a2d2-2e34-4f68-b899-6e013af77a21",
      "table_name": "PROJECT",
      "record_id": "90aeb75e-807f-4682-825e-f84ab4ab8315",
      "record_pk": {
        "id": "90aeb75e-807f-4682-825e-f84ab4ab8315"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "90aeb75e-807f-4682-825e-f84ab4ab8315",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T01:59:52.329558+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:59:52.329558+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "cc7c71e4-1ee9-417c-b401-e8a7fa67d240",
      "table_name": "PROJECT",
      "record_id": "ab6ccada-dcb2-4554-8748-2a95fb69bd78",
      "record_pk": {
        "id": "ab6ccada-dcb2-4554-8748-2a95fb69bd78"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "ab6ccada-dcb2-4554-8748-2a95fb69bd78",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T01:59:52.096438+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:59:52.096438+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f06f9dff-ff18-446a-836e-ae5a089e59a1",
      "table_name": "PROJECT",
      "record_id": "777ea3f0-e225-4fc5-b327-839d6d03ef61",
      "record_pk": {
        "id": "777ea3f0-e225-4fc5-b327-839d6d03ef61"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "777ea3f0-e225-4fc5-b327-839d6d03ef61",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T01:59:40.012927+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:59:51.366831+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "178d100f-5265-44ba-903a-99e925bdd3ea",
      "table_name": "PROJECT",
      "record_id": "359c985a-4b7a-4079-ae0f-ca22594156e5",
      "record_pk": {
        "id": "359c985a-4b7a-4079-ae0f-ca22594156e5"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "359c985a-4b7a-4079-ae0f-ca22594156e5",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T01:59:40.365094+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:59:51.118949+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "65a5ef64-11e4-4b2e-ad98-4e3033a69907",
      "table_name": "PROJECT",
      "record_id": "359c985a-4b7a-4079-ae0f-ca22594156e5",
      "record_pk": {
        "id": "359c985a-4b7a-4079-ae0f-ca22594156e5"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "359c985a-4b7a-4079-ae0f-ca22594156e5",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T01:59:40.365094+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:59:40.365094+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "be7e2891-ab50-4497-b6b1-4b29a1e7bbcc",
      "table_name": "PROJECT",
      "record_id": "777ea3f0-e225-4fc5-b327-839d6d03ef61",
      "record_pk": {
        "id": "777ea3f0-e225-4fc5-b327-839d6d03ef61"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "777ea3f0-e225-4fc5-b327-839d6d03ef61",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T01:59:40.012927+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:59:40.012927+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9944d62e-9f55-429d-921d-61a370b4448c",
      "table_name": "PROJECT",
      "record_id": "1acf29e1-9f75-446c-bf1c-b1bc98999742",
      "record_pk": {
        "id": "1acf29e1-9f75-446c-bf1c-b1bc98999742"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "1acf29e1-9f75-446c-bf1c-b1bc98999742",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T01:32:44.751337+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:33:21.035641+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a1444389-3528-4b3c-90b2-67eea3e4cbfc",
      "table_name": "PROJECT",
      "record_id": "1acf29e1-9f75-446c-bf1c-b1bc98999742",
      "record_pk": {
        "id": "1acf29e1-9f75-446c-bf1c-b1bc98999742"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "1acf29e1-9f75-446c-bf1c-b1bc98999742",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T01:32:44.751337+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:44.751337+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "2ba67a40-178f-4cea-9e94-aa065ace073b",
      "table_name": "PROJECT",
      "record_id": "89437825-6c33-44b3-9d11-df1272fb0c3e",
      "record_pk": {
        "id": "89437825-6c33-44b3-9d11-df1272fb0c3e"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "89437825-6c33-44b3-9d11-df1272fb0c3e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T01:32:31.943957+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:43.520859+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "be82f6ee-9b7f-4d29-9344-7436c5a0509f",
      "table_name": "PROJECT",
      "record_id": "89437825-6c33-44b3-9d11-df1272fb0c3e",
      "record_pk": {
        "id": "89437825-6c33-44b3-9d11-df1272fb0c3e"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "89437825-6c33-44b3-9d11-df1272fb0c3e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T01:32:31.943957+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:31.943957+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d5e76a0b-d190-4c2c-a129-8a2cf76ea0b4",
      "table_name": "PROJECT",
      "record_id": "9d58f016-6410-4fdc-99a9-735e64e532c5",
      "record_pk": {
        "id": "9d58f016-6410-4fdc-99a9-735e64e532c5"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "9d58f016-6410-4fdc-99a9-735e64e532c5",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T01:32:18.094283+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:31.208253+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "664a8845-e84c-4809-8611-a9a1ddcf0ad5",
      "table_name": "PROJECT",
      "record_id": "53ceb1c5-7d43-4141-8ca8-7efd5ba088af",
      "record_pk": {
        "id": "53ceb1c5-7d43-4141-8ca8-7efd5ba088af"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "53ceb1c5-7d43-4141-8ca8-7efd5ba088af",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T01:32:18.520512+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:30.964965+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "acf24595-034f-4350-be6a-96925dc1d226",
      "table_name": "PROJECT",
      "record_id": "53ceb1c5-7d43-4141-8ca8-7efd5ba088af",
      "record_pk": {
        "id": "53ceb1c5-7d43-4141-8ca8-7efd5ba088af"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "53ceb1c5-7d43-4141-8ca8-7efd5ba088af",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T01:32:18.520512+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:18.520512+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "45c7b621-8411-4533-a027-9d36dde1d7fa",
      "table_name": "PROJECT",
      "record_id": "9d58f016-6410-4fdc-99a9-735e64e532c5",
      "record_pk": {
        "id": "9d58f016-6410-4fdc-99a9-735e64e532c5"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "9d58f016-6410-4fdc-99a9-735e64e532c5",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T01:32:18.094283+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:18.094283+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "dbc06094-d4c5-4670-9848-a557d1d009ab",
      "table_name": "PROJECT",
      "record_id": "80f01557-d86b-4239-b4af-531d4dc473e8",
      "record_pk": {
        "id": "80f01557-d86b-4239-b4af-531d4dc473e8"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "80f01557-d86b-4239-b4af-531d4dc473e8",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T01:32:04.589827+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:17.354434+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "38d76bb7-b77f-4cf9-b6d7-03a2ed6b1a62",
      "table_name": "PROJECT",
      "record_id": "9eb31356-812a-4ccf-a829-e39171d43a8f",
      "record_pk": {
        "id": "9eb31356-812a-4ccf-a829-e39171d43a8f"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "9eb31356-812a-4ccf-a829-e39171d43a8f",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T01:32:04.827447+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:17.114075+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "3c74b5ba-6a26-48e4-aae5-b88eda836321",
      "table_name": "PROJECT",
      "record_id": "9eb31356-812a-4ccf-a829-e39171d43a8f",
      "record_pk": {
        "id": "9eb31356-812a-4ccf-a829-e39171d43a8f"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "9eb31356-812a-4ccf-a829-e39171d43a8f",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T01:32:04.827447+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:04.827447+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a89d6f7b-a0a2-4cb2-a8aa-c58ffa1d2d0e",
      "table_name": "PROJECT",
      "record_id": "80f01557-d86b-4239-b4af-531d4dc473e8",
      "record_pk": {
        "id": "80f01557-d86b-4239-b4af-531d4dc473e8"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "80f01557-d86b-4239-b4af-531d4dc473e8",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T01:32:04.589827+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:32:04.589827+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "b3db8a64-f121-43a3-b507-ba1d33bb5b21",
      "table_name": "PROJECT",
      "record_id": "2644b4c6-61e1-48d2-9531-1df42142b3f7",
      "record_pk": {
        "id": "2644b4c6-61e1-48d2-9531-1df42142b3f7"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "2644b4c6-61e1-48d2-9531-1df42142b3f7",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T01:29:40.816691+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:29:40.816691+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "966ea83d-4de7-48cd-a60d-7beb6a94c63e",
      "table_name": "PROJECT",
      "record_id": "1ebfba1a-afa0-4bc0-9cc3-1bfd0f7acad7",
      "record_pk": {
        "id": "1ebfba1a-afa0-4bc0-9cc3-1bfd0f7acad7"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "1ebfba1a-afa0-4bc0-9cc3-1bfd0f7acad7",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T01:29:40.480486+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:29:40.480486+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c8160953-ea63-479a-8305-2414617e8af5",
      "table_name": "PROJECT",
      "record_id": "d1322234-25e6-4329-b994-feb5b2b4e5c1",
      "record_pk": {
        "id": "d1322234-25e6-4329-b994-feb5b2b4e5c1"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "d1322234-25e6-4329-b994-feb5b2b4e5c1",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T01:00:09.878283+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:00:09.948085+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "94aa319e-1686-43c7-adb5-c413c455303d",
      "table_name": "PROJECT",
      "record_id": "d1322234-25e6-4329-b994-feb5b2b4e5c1",
      "record_pk": {
        "id": "d1322234-25e6-4329-b994-feb5b2b4e5c1"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "d1322234-25e6-4329-b994-feb5b2b4e5c1",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T01:00:09.878283+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:00:09.878283+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d6c67155-0135-4506-b635-00410e35503b",
      "table_name": "PROJECT",
      "record_id": "860aeeca-98c6-4c9b-8d80-069cac20277e",
      "record_pk": {
        "id": "860aeeca-98c6-4c9b-8d80-069cac20277e"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "860aeeca-98c6-4c9b-8d80-069cac20277e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:59:57.92019+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T01:00:08.818078+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0ab55f54-3c15-4b91-847a-e58f20232c16",
      "table_name": "PROJECT",
      "record_id": "860aeeca-98c6-4c9b-8d80-069cac20277e",
      "record_pk": {
        "id": "860aeeca-98c6-4c9b-8d80-069cac20277e"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "860aeeca-98c6-4c9b-8d80-069cac20277e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:59:57.92019+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:59:57.92019+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "249c1528-b35d-47c1-87da-3ec770ad016a",
      "table_name": "PROJECT",
      "record_id": "c9e0e694-7eab-40ef-96f6-788258327588",
      "record_pk": {
        "id": "c9e0e694-7eab-40ef-96f6-788258327588"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "c9e0e694-7eab-40ef-96f6-788258327588",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:59:48.736318+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:59:57.367297+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "607e45dc-265f-42f6-86d0-25c5d2014506",
      "table_name": "PROJECT",
      "record_id": "c35cc1c9-e8fd-435e-bfc4-c9627c595e4f",
      "record_pk": {
        "id": "c35cc1c9-e8fd-435e-bfc4-c9627c595e4f"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "c35cc1c9-e8fd-435e-bfc4-c9627c595e4f",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:59:48.783748+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:59:57.32344+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "33f0c0c1-6251-4c7d-b64f-a4ecdccdae38",
      "table_name": "PROJECT",
      "record_id": "c35cc1c9-e8fd-435e-bfc4-c9627c595e4f",
      "record_pk": {
        "id": "c35cc1c9-e8fd-435e-bfc4-c9627c595e4f"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "c35cc1c9-e8fd-435e-bfc4-c9627c595e4f",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:59:48.783748+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:59:48.783748+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0eb76ca0-3828-4852-9669-8130b8c1dc87",
      "table_name": "PROJECT",
      "record_id": "c9e0e694-7eab-40ef-96f6-788258327588",
      "record_pk": {
        "id": "c9e0e694-7eab-40ef-96f6-788258327588"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "c9e0e694-7eab-40ef-96f6-788258327588",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:59:48.736318+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:59:48.736318+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f9274f57-c3ef-4436-aa37-1c71ff9f3a87",
      "table_name": "PROJECT",
      "record_id": "71ff6655-bd83-4491-b399-6b859a8fef77",
      "record_pk": {
        "id": "71ff6655-bd83-4491-b399-6b859a8fef77"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "71ff6655-bd83-4491-b399-6b859a8fef77",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:59:36.112176+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:59:48.182945+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7cbd89ec-34b9-4f14-ae1d-7b049a745b0d",
      "table_name": "PROJECT",
      "record_id": "85c470a6-a4ad-4936-88b6-042538dda2a2",
      "record_pk": {
        "id": "85c470a6-a4ad-4936-88b6-042538dda2a2"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "85c470a6-a4ad-4936-88b6-042538dda2a2",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:59:36.202052+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:59:48.130317+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "aab0ec89-24d5-483e-a6a7-2cb82e319462",
      "table_name": "PROJECT",
      "record_id": "85c470a6-a4ad-4936-88b6-042538dda2a2",
      "record_pk": {
        "id": "85c470a6-a4ad-4936-88b6-042538dda2a2"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "85c470a6-a4ad-4936-88b6-042538dda2a2",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:59:36.202052+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:59:36.202052+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "731efb27-39ce-48cd-8a35-8f2eb88bfa62",
      "table_name": "PROJECT",
      "record_id": "71ff6655-bd83-4491-b399-6b859a8fef77",
      "record_pk": {
        "id": "71ff6655-bd83-4491-b399-6b859a8fef77"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "71ff6655-bd83-4491-b399-6b859a8fef77",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:59:36.112176+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:59:36.112176+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7e8544b5-c8c4-457d-9284-d659604b156c",
      "table_name": "PROJECT",
      "record_id": "a380bab4-8edf-41eb-a4e8-5b99d058b7ab",
      "record_pk": {
        "id": "a380bab4-8edf-41eb-a4e8-5b99d058b7ab"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "a380bab4-8edf-41eb-a4e8-5b99d058b7ab",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T00:45:41.414762+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:41.599245+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f8dd85ce-71c8-4966-93e6-dcc1d54f9a68",
      "table_name": "PROJECT",
      "record_id": "a380bab4-8edf-41eb-a4e8-5b99d058b7ab",
      "record_pk": {
        "id": "a380bab4-8edf-41eb-a4e8-5b99d058b7ab"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "a380bab4-8edf-41eb-a4e8-5b99d058b7ab",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T00:45:41.414762+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:41.414762+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "db336435-73b0-418e-83a3-edd8a5a39a63",
      "table_name": "PROJECT",
      "record_id": "5f01473c-137f-4841-8b52-52f9fe3781f6",
      "record_pk": {
        "id": "5f01473c-137f-4841-8b52-52f9fe3781f6"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "5f01473c-137f-4841-8b52-52f9fe3781f6",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:45:28.318047+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:40.363495+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8513542d-5ad7-4d55-beee-c523931c118f",
      "table_name": "PROJECT",
      "record_id": "5f01473c-137f-4841-8b52-52f9fe3781f6",
      "record_pk": {
        "id": "5f01473c-137f-4841-8b52-52f9fe3781f6"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "5f01473c-137f-4841-8b52-52f9fe3781f6",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:45:28.318047+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:28.318047+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "475e8481-aca1-478a-8095-25c08af598fe",
      "table_name": "PROJECT",
      "record_id": "553910a4-764a-4062-a271-0513c793ead3",
      "record_pk": {
        "id": "553910a4-764a-4062-a271-0513c793ead3"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "553910a4-764a-4062-a271-0513c793ead3",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:45:19.609907+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:27.766159+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "5e629cdc-c04e-4a6d-b9fb-dfe36566af5a",
      "table_name": "PROJECT",
      "record_id": "afdae585-d4ad-436a-9748-7fad5c045459",
      "record_pk": {
        "id": "afdae585-d4ad-436a-9748-7fad5c045459"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "afdae585-d4ad-436a-9748-7fad5c045459",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:45:19.653984+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:27.721413+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a036ba2b-776c-4dbf-a8ed-9c9cc054c2b4",
      "table_name": "PROJECT",
      "record_id": "afdae585-d4ad-436a-9748-7fad5c045459",
      "record_pk": {
        "id": "afdae585-d4ad-436a-9748-7fad5c045459"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "afdae585-d4ad-436a-9748-7fad5c045459",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:45:19.653984+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:19.653984+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "23508288-87d9-4c06-ad9e-a12c99a3acee",
      "table_name": "PROJECT",
      "record_id": "553910a4-764a-4062-a271-0513c793ead3",
      "record_pk": {
        "id": "553910a4-764a-4062-a271-0513c793ead3"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "553910a4-764a-4062-a271-0513c793ead3",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:45:19.609907+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:19.609907+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d0615411-e3ce-4bc1-b696-8256e0afa3ff",
      "table_name": "PROJECT",
      "record_id": "0ba3b512-33b7-4e3a-a109-5e2a54373971",
      "record_pk": {
        "id": "0ba3b512-33b7-4e3a-a109-5e2a54373971"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "0ba3b512-33b7-4e3a-a109-5e2a54373971",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:45:08.285235+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:19.057241+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0c23e443-bbaa-4891-b66b-13d5f5a87902",
      "table_name": "PROJECT",
      "record_id": "21971e05-b4c6-4b27-a028-fc87fcb8ab73",
      "record_pk": {
        "id": "21971e05-b4c6-4b27-a028-fc87fcb8ab73"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "21971e05-b4c6-4b27-a028-fc87fcb8ab73",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:45:08.345592+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:19.014609+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f4a370a1-aa88-4f6f-96ba-19c21a4f7b9b",
      "table_name": "PROJECT",
      "record_id": "21971e05-b4c6-4b27-a028-fc87fcb8ab73",
      "record_pk": {
        "id": "21971e05-b4c6-4b27-a028-fc87fcb8ab73"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "21971e05-b4c6-4b27-a028-fc87fcb8ab73",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:45:08.345592+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:08.345592+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ea3b4d69-d3cb-48cd-9c16-c0d59b4fe2fb",
      "table_name": "PROJECT",
      "record_id": "0ba3b512-33b7-4e3a-a109-5e2a54373971",
      "record_pk": {
        "id": "0ba3b512-33b7-4e3a-a109-5e2a54373971"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "0ba3b512-33b7-4e3a-a109-5e2a54373971",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:45:08.285235+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:45:08.285235+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9cb99ef4-0dc5-4095-8291-3780c041dcb7",
      "table_name": "PROJECT",
      "record_id": "0ca23f76-55f2-43ca-989b-e616dae56fbe",
      "record_pk": {
        "id": "0ca23f76-55f2-43ca-989b-e616dae56fbe"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "0ca23f76-55f2-43ca-989b-e616dae56fbe",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T00:40:46.19996+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:46.337428+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "b8aaab4a-c4c5-4083-a4c2-bf54abe078eb",
      "table_name": "PROJECT",
      "record_id": "0ca23f76-55f2-43ca-989b-e616dae56fbe",
      "record_pk": {
        "id": "0ca23f76-55f2-43ca-989b-e616dae56fbe"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "0ca23f76-55f2-43ca-989b-e616dae56fbe",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T00:40:46.19996+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:46.19996+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "557b609a-0378-4380-b233-6e3d882291cf",
      "table_name": "PROJECT",
      "record_id": "91b2ac4a-b547-463c-9b68-f63c04ecf3ab",
      "record_pk": {
        "id": "91b2ac4a-b547-463c-9b68-f63c04ecf3ab"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "91b2ac4a-b547-463c-9b68-f63c04ecf3ab",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:40:33.682554+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:45.029904+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ad3ac627-d76a-4e03-9025-d850e542e7f6",
      "table_name": "PROJECT",
      "record_id": "91b2ac4a-b547-463c-9b68-f63c04ecf3ab",
      "record_pk": {
        "id": "91b2ac4a-b547-463c-9b68-f63c04ecf3ab"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "91b2ac4a-b547-463c-9b68-f63c04ecf3ab",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:40:33.682554+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:33.682554+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "13a4fe8c-c1e2-4c06-b9b6-8fd206aec776",
      "table_name": "PROJECT",
      "record_id": "6ab72a42-7bab-4e06-8330-84e9f12cef42",
      "record_pk": {
        "id": "6ab72a42-7bab-4e06-8330-84e9f12cef42"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "6ab72a42-7bab-4e06-8330-84e9f12cef42",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:40:25.759141+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:33.122108+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "042b5a53-69b2-4001-bbff-cbd15842fefe",
      "table_name": "PROJECT",
      "record_id": "3c4e6090-5e64-4d36-bb56-e17e95012a8e",
      "record_pk": {
        "id": "3c4e6090-5e64-4d36-bb56-e17e95012a8e"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "3c4e6090-5e64-4d36-bb56-e17e95012a8e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:40:25.813938+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:33.076071+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "390c4382-f8f1-4b31-b9f3-66cb684f664e",
      "table_name": "PROJECT",
      "record_id": "3c4e6090-5e64-4d36-bb56-e17e95012a8e",
      "record_pk": {
        "id": "3c4e6090-5e64-4d36-bb56-e17e95012a8e"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "3c4e6090-5e64-4d36-bb56-e17e95012a8e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:40:25.813938+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:25.813938+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "3b90e7e4-e474-430f-b34c-d1fa98d77a59",
      "table_name": "PROJECT",
      "record_id": "6ab72a42-7bab-4e06-8330-84e9f12cef42",
      "record_pk": {
        "id": "6ab72a42-7bab-4e06-8330-84e9f12cef42"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "6ab72a42-7bab-4e06-8330-84e9f12cef42",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:40:25.759141+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:25.759141+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d51461cd-7415-4d0e-946c-bf3d142f7bdc",
      "table_name": "PROJECT",
      "record_id": "e3082416-ae9f-4f86-8f4d-f0666c628dd8",
      "record_pk": {
        "id": "e3082416-ae9f-4f86-8f4d-f0666c628dd8"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "e3082416-ae9f-4f86-8f4d-f0666c628dd8",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:40:15.027395+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:25.200362+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "67fd4b48-7350-4d61-85ee-90134061e05a",
      "table_name": "PROJECT",
      "record_id": "c783d237-ba40-4a32-94f9-e7c856112a57",
      "record_pk": {
        "id": "c783d237-ba40-4a32-94f9-e7c856112a57"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "c783d237-ba40-4a32-94f9-e7c856112a57",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:40:15.08094+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:25.157074+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "3de1bfec-c821-420b-831d-40daa408146c",
      "table_name": "PROJECT",
      "record_id": "c783d237-ba40-4a32-94f9-e7c856112a57",
      "record_pk": {
        "id": "c783d237-ba40-4a32-94f9-e7c856112a57"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "c783d237-ba40-4a32-94f9-e7c856112a57",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:40:15.08094+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:15.08094+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "aeca6a80-9a51-4e29-b69e-041a4f0679cc",
      "table_name": "PROJECT",
      "record_id": "e3082416-ae9f-4f86-8f4d-f0666c628dd8",
      "record_pk": {
        "id": "e3082416-ae9f-4f86-8f4d-f0666c628dd8"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "e3082416-ae9f-4f86-8f4d-f0666c628dd8",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:40:15.027395+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:40:15.027395+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f0e4d9b3-635d-4383-b4a9-e2c011926748",
      "table_name": "PROJECT",
      "record_id": "cf1b0bbf-f5a4-4ee5-842b-9b1b778c649d",
      "record_pk": {
        "id": "cf1b0bbf-f5a4-4ee5-842b-9b1b778c649d"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "cf1b0bbf-f5a4-4ee5-842b-9b1b778c649d",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T00:37:08.850147+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:37:42.65806+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "2b9f7864-9539-45b7-9724-ff0cfd4be102",
      "table_name": "PROJECT",
      "record_id": "cf1b0bbf-f5a4-4ee5-842b-9b1b778c649d",
      "record_pk": {
        "id": "cf1b0bbf-f5a4-4ee5-842b-9b1b778c649d"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "cf1b0bbf-f5a4-4ee5-842b-9b1b778c649d",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T00:37:08.850147+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:37:08.850147+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9f05cbc6-b4fb-4983-83e8-6234c311059d",
      "table_name": "PROJECT",
      "record_id": "5841de74-485e-417e-bad2-aa2c41c53377",
      "record_pk": {
        "id": "5841de74-485e-417e-bad2-aa2c41c53377"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "5841de74-485e-417e-bad2-aa2c41c53377",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:36:55.224959+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:37:07.554434+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "79ff46e6-0ff7-4c49-878b-ea7b0a0aeda9",
      "table_name": "PROJECT",
      "record_id": "5841de74-485e-417e-bad2-aa2c41c53377",
      "record_pk": {
        "id": "5841de74-485e-417e-bad2-aa2c41c53377"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "5841de74-485e-417e-bad2-aa2c41c53377",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:36:55.224959+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:55.224959+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ebf6431c-c80a-45cf-8c23-b36e9a212d25",
      "table_name": "PROJECT",
      "record_id": "c9ffc77f-8da6-4d38-a673-6f3d3eca306e",
      "record_pk": {
        "id": "c9ffc77f-8da6-4d38-a673-6f3d3eca306e"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "c9ffc77f-8da6-4d38-a673-6f3d3eca306e",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:36:41.299559+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:54.249718+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "210b0d9b-367f-48aa-bac0-c1087b72524f",
      "table_name": "PROJECT",
      "record_id": "a9addf70-c3a8-45f9-82e3-1dda34d3c76b",
      "record_pk": {
        "id": "a9addf70-c3a8-45f9-82e3-1dda34d3c76b"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "a9addf70-c3a8-45f9-82e3-1dda34d3c76b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:36:41.587687+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:53.914937+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "14d4bb89-d968-47fe-8cd8-8f9478abeedb",
      "table_name": "PROJECT",
      "record_id": "a9addf70-c3a8-45f9-82e3-1dda34d3c76b",
      "record_pk": {
        "id": "a9addf70-c3a8-45f9-82e3-1dda34d3c76b"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "a9addf70-c3a8-45f9-82e3-1dda34d3c76b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:36:41.587687+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:41.587687+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8ca4105a-4d58-46a7-8419-90fdc23c62cb",
      "table_name": "PROJECT",
      "record_id": "c9ffc77f-8da6-4d38-a673-6f3d3eca306e",
      "record_pk": {
        "id": "c9ffc77f-8da6-4d38-a673-6f3d3eca306e"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "c9ffc77f-8da6-4d38-a673-6f3d3eca306e",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:36:41.299559+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:41.299559+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d462f09a-06ba-406f-8eae-d2e3b7803cc0",
      "table_name": "PROJECT",
      "record_id": "bd21cafc-f5ac-4497-8c99-4d87a5b7952f",
      "record_pk": {
        "id": "bd21cafc-f5ac-4497-8c99-4d87a5b7952f"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "bd21cafc-f5ac-4497-8c99-4d87a5b7952f",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:36:28.827004+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:40.497065+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e4743605-a69d-4182-be06-3ec72f34b318",
      "table_name": "PROJECT",
      "record_id": "ec501458-197f-4327-bbca-c438aa456fe3",
      "record_pk": {
        "id": "ec501458-197f-4327-bbca-c438aa456fe3"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "ec501458-197f-4327-bbca-c438aa456fe3",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:36:29.172558+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:40.205585+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "eb0f7d04-883a-4d1f-ad27-8a683d65e500",
      "table_name": "PROJECT",
      "record_id": "8a584961-beb1-4f12-b00a-e43b472c2389",
      "record_pk": {
        "id": "8a584961-beb1-4f12-b00a-e43b472c2389"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "8a584961-beb1-4f12-b00a-e43b472c2389",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T00:36:34.530768+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:34.623425+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6e08e5bf-a802-4d73-a4df-e07ccccda55d",
      "table_name": "PROJECT",
      "record_id": "8a584961-beb1-4f12-b00a-e43b472c2389",
      "record_pk": {
        "id": "8a584961-beb1-4f12-b00a-e43b472c2389"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "8a584961-beb1-4f12-b00a-e43b472c2389",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-07T00:36:34.530768+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:34.530768+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8c1bcf38-ac8d-48da-9c35-d32c304e1a8b",
      "table_name": "PROJECT",
      "record_id": "8555a817-1d1e-4b8c-8777-657bf5ecf10b",
      "record_pk": {
        "id": "8555a817-1d1e-4b8c-8777-657bf5ecf10b"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "8555a817-1d1e-4b8c-8777-657bf5ecf10b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:36:26.097681+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:33.48177+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d64d74e2-11b2-4789-bff5-6962b90fbb25",
      "table_name": "PROJECT",
      "record_id": "ec501458-197f-4327-bbca-c438aa456fe3",
      "record_pk": {
        "id": "ec501458-197f-4327-bbca-c438aa456fe3"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "ec501458-197f-4327-bbca-c438aa456fe3",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:36:29.172558+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:29.172558+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "66d88bf9-9f0c-4928-aac1-db3d8700e7b1",
      "table_name": "PROJECT",
      "record_id": "bd21cafc-f5ac-4497-8c99-4d87a5b7952f",
      "record_pk": {
        "id": "bd21cafc-f5ac-4497-8c99-4d87a5b7952f"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "bd21cafc-f5ac-4497-8c99-4d87a5b7952f",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:36:28.827004+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:28.827004+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6dfdb846-9e7a-4777-ac6b-3ee67e566f77",
      "table_name": "PROJECT",
      "record_id": "8555a817-1d1e-4b8c-8777-657bf5ecf10b",
      "record_pk": {
        "id": "8555a817-1d1e-4b8c-8777-657bf5ecf10b"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "8555a817-1d1e-4b8c-8777-657bf5ecf10b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-07T00:36:26.097681+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:26.097681+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "783d49d1-2908-4ca4-8788-879624cee5a5",
      "table_name": "PROJECT",
      "record_id": "5dd0a593-d926-4af4-a360-2a2e64898b75",
      "record_pk": {
        "id": "5dd0a593-d926-4af4-a360-2a2e64898b75"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "5dd0a593-d926-4af4-a360-2a2e64898b75",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:36:20.508019+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:25.541681+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "87c7d047-941e-4aa4-91a6-480c71fa3239",
      "table_name": "PROJECT",
      "record_id": "635354dd-6acb-422b-8d72-8b706818102c",
      "record_pk": {
        "id": "635354dd-6acb-422b-8d72-8b706818102c"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "635354dd-6acb-422b-8d72-8b706818102c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:36:20.564891+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:25.503344+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "df11f3d5-4e24-409d-9bb2-e63957b9bd23",
      "table_name": "PROJECT",
      "record_id": "635354dd-6acb-422b-8d72-8b706818102c",
      "record_pk": {
        "id": "635354dd-6acb-422b-8d72-8b706818102c"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "635354dd-6acb-422b-8d72-8b706818102c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-07T00:36:20.564891+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:20.564891+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "42ee4eff-cf88-4a80-8273-a9abd20e7096",
      "table_name": "PROJECT",
      "record_id": "5dd0a593-d926-4af4-a360-2a2e64898b75",
      "record_pk": {
        "id": "5dd0a593-d926-4af4-a360-2a2e64898b75"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "5dd0a593-d926-4af4-a360-2a2e64898b75",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-07T00:36:20.508019+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:20.508019+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ad90d512-5c9f-4d72-85ac-1e7be18bf3e2",
      "table_name": "PROJECT",
      "record_id": "658c334e-ef5d-4806-9400-2e61d3fd25c5",
      "record_pk": {
        "id": "658c334e-ef5d-4806-9400-2e61d3fd25c5"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "658c334e-ef5d-4806-9400-2e61d3fd25c5",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:36:08.920841+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:19.957881+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ebabe7cb-5f45-4eb2-b4d0-d5890b7b0ce7",
      "table_name": "PROJECT",
      "record_id": "bcf76465-29f2-44d0-84e9-2b241748bde4",
      "record_pk": {
        "id": "bcf76465-29f2-44d0-84e9-2b241748bde4"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "bcf76465-29f2-44d0-84e9-2b241748bde4",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:36:09.07307+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:19.900168+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4c1c975d-19a8-4975-a609-b5fe0ee5a971",
      "table_name": "PROJECT",
      "record_id": "bcf76465-29f2-44d0-84e9-2b241748bde4",
      "record_pk": {
        "id": "bcf76465-29f2-44d0-84e9-2b241748bde4"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "bcf76465-29f2-44d0-84e9-2b241748bde4",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-07T00:36:09.07307+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:09.07307+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ad6b9ec1-bd1a-48f9-ae9c-c8fba008a161",
      "table_name": "PROJECT",
      "record_id": "658c334e-ef5d-4806-9400-2e61d3fd25c5",
      "record_pk": {
        "id": "658c334e-ef5d-4806-9400-2e61d3fd25c5"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "658c334e-ef5d-4806-9400-2e61d3fd25c5",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-07T00:36:08.920841+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-07T00:36:08.920841+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "b7cd2e3f-84db-4b7e-b1b8-61912b0b9d6d",
      "table_name": "PROJECT",
      "record_id": "4500855f-fa31-4630-84a6-669ac732320e",
      "record_pk": {
        "id": "4500855f-fa31-4630-84a6-669ac732320e"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "4500855f-fa31-4630-84a6-669ac732320e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-06T23:19:05.242786+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:19:37.278772+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "58dd5210-a8c2-4639-937d-9a728fb554f8",
      "table_name": "PROJECT",
      "record_id": "4500855f-fa31-4630-84a6-669ac732320e",
      "record_pk": {
        "id": "4500855f-fa31-4630-84a6-669ac732320e"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "4500855f-fa31-4630-84a6-669ac732320e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-enrich",
        "members": [],
        "created_at": "2025-11-06T23:19:05.242786+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:19:05.242786+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "40f9b30c-f5c1-4808-b239-870f92a83eb1",
      "table_name": "PROJECT",
      "record_id": "ee3e8114-3d67-440c-8b3b-a00ab204066f",
      "record_pk": {
        "id": "ee3e8114-3d67-440c-8b3b-a00ab204066f"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "ee3e8114-3d67-440c-8b3b-a00ab204066f",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-06T23:18:51.613114+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:19:03.93051+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f2fe562e-ccd3-45e9-add2-02bfba39554c",
      "table_name": "PROJECT",
      "record_id": "ee3e8114-3d67-440c-8b3b-a00ab204066f",
      "record_pk": {
        "id": "ee3e8114-3d67-440c-8b3b-a00ab204066f"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "ee3e8114-3d67-440c-8b3b-a00ab204066f",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-dept",
        "members": [],
        "created_at": "2025-11-06T23:18:51.613114+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:18:51.613114+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "1eeba95d-5227-407b-9782-138bddbb7dd8",
      "table_name": "PROJECT",
      "record_id": "bffe0e63-8ba5-429d-9a8a-8569a614a2eb",
      "record_pk": {
        "id": "bffe0e63-8ba5-429d-9a8a-8569a614a2eb"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "bffe0e63-8ba5-429d-9a8a-8569a614a2eb",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-06T23:18:37.072731+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:18:50.729762+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "32014864-f783-4556-9129-ed6204f57a93",
      "table_name": "PROJECT",
      "record_id": "61ba26de-64b7-4585-9fef-03f39750b60a",
      "record_pk": {
        "id": "61ba26de-64b7-4585-9fef-03f39750b60a"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "61ba26de-64b7-4585-9fef-03f39750b60a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-06T23:18:37.391432+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:18:49.738397+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e56a30c1-d78a-4b59-90f6-bd8b18ce1ec1",
      "table_name": "PROJECT",
      "record_id": "61ba26de-64b7-4585-9fef-03f39750b60a",
      "record_pk": {
        "id": "61ba26de-64b7-4585-9fef-03f39750b60a"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "61ba26de-64b7-4585-9fef-03f39750b60a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": null,
        "name": "itest-member",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-06T23:18:37.391432+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:18:37.391432+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c226885e-3838-420b-99ba-b92dd1267b09",
      "table_name": "PROJECT",
      "record_id": "bffe0e63-8ba5-429d-9a8a-8569a614a2eb",
      "record_pk": {
        "id": "bffe0e63-8ba5-429d-9a8a-8569a614a2eb"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "bffe0e63-8ba5-429d-9a8a-8569a614a2eb",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": null,
        "name": "itest-owned",
        "members": [],
        "created_at": "2025-11-06T23:18:37.072731+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:18:37.072731+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "2d4f150c-ab26-448e-a4bf-522b86798fde",
      "table_name": "PROJECT",
      "record_id": "4ec80b6d-61ff-4b5d-a6f9-3b1176bc21c1",
      "record_pk": {
        "id": "4ec80b6d-61ff-4b5d-a6f9-3b1176bc21c1"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "4ec80b6d-61ff-4b5d-a6f9-3b1176bc21c1",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-06T23:18:24.572762+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:18:36.267292+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "26e5aca3-dcac-47b3-b4d8-c4b9d43270cd",
      "table_name": "PROJECT",
      "record_id": "b71fc167-aa27-4310-a208-816c6a2f8830",
      "record_pk": {
        "id": "b71fc167-aa27-4310-a208-816c6a2f8830"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "b71fc167-aa27-4310-a208-816c6a2f8830",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-06T23:18:24.951935+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:18:35.956682+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a2677113-dcab-4364-9a93-e2da78218805",
      "table_name": "PROJECT",
      "record_id": "b71fc167-aa27-4310-a208-816c6a2f8830",
      "record_pk": {
        "id": "b71fc167-aa27-4310-a208-816c6a2f8830"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "b71fc167-aa27-4310-a208-816c6a2f8830",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-2",
        "members": [],
        "created_at": "2025-11-06T23:18:24.951935+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:18:24.951935+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "19b7ed0b-477d-4f0e-ac14-c3935f87e0d1",
      "table_name": "PROJECT",
      "record_id": "4ec80b6d-61ff-4b5d-a6f9-3b1176bc21c1",
      "record_pk": {
        "id": "4ec80b6d-61ff-4b5d-a6f9-3b1176bc21c1"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "4ec80b6d-61ff-4b5d-a6f9-3b1176bc21c1",
        "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
        "desc": null,
        "name": "itest-all-1",
        "members": [],
        "created_at": "2025-11-06T23:18:24.572762+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T23:18:24.572762+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "bb9d02f1-4895-4ff7-a316-52d7062a535a",
      "table_name": "PROJECT",
      "record_id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
      "record_pk": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING JW CY DONT AMEND",
        "members": [],
        "created_at": "2025-11-06T22:07:01.818074+00:00"
      },
      "new_values": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING JW CY DONT AMEND",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458"
        ],
        "created_at": "2025-11-06T22:07:01.818074+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "6933d965-e4c4-4b49-bc99-08236b1d9458"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-11-06T22:46:33.478295+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "02c2b435-76cc-40d8-ab91-2e5f26896995",
      "table_name": "PROJECT",
      "record_id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
      "record_pk": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING JW CY DONT AMEND",
        "members": [],
        "created_at": "2025-11-06T22:07:01.818074+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T22:07:01.818074+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ce49049a-e4c7-4da4-8ab0-1f8fecba8921",
      "table_name": "PROJECT",
      "record_id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
      "record_pk": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "new_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "6933d965-e4c4-4b49-bc99-08236b1d9458",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "6933d965-e4c4-4b49-bc99-08236b1d9458",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-06T21:53:50.809628+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "5f000ae4-1466-4f1f-b8c5-a111cef6005d",
      "table_name": "PROJECT",
      "record_id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
      "record_pk": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "new_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "6933d965-e4c4-4b49-bc99-08236b1d9458",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "6933d965-e4c4-4b49-bc99-08236b1d9458",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-06T21:06:36.428398+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0f32e190-efca-4f32-80cf-e786e04a5a52",
      "table_name": "PROJECT",
      "record_id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
      "record_pk": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "new_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "6933d965-e4c4-4b49-bc99-08236b1d9458",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "6933d965-e4c4-4b49-bc99-08236b1d9458"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-06T18:12:18.102354+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "16c5231d-3087-488d-88e3-07dc2aa0271f",
      "table_name": "PROJECT",
      "record_id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
      "record_pk": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND T^T",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "new_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "changed_fields": [
        "name"
      ],
      "delta": {
        "name": {
          "new": "TESTING PLS DONT AMEND",
          "old": "TESTING PLS DONT AMEND T^T"
        }
      },
      "user_id": null,
      "timestamp": "2025-11-06T07:47:32.125707+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "007dd5ce-0a23-42fb-9f4e-d18f6ee69270",
      "table_name": "PROJECT",
      "record_id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
      "record_pk": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
        "uid": "765bc84f-eba5-4d32-987b-d55adef7fe65",
        "desc": "tested to make it work, killed two views for this and it works",
        "name": "create to make sure default values work pls work",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-11-05T19:09:59.689236+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T07:16:27.491163+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "715d297c-e403-4d4a-9af9-658daa3f5b12",
      "table_name": "PROJECT",
      "record_id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
      "record_pk": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND T^T",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "new_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND T^T",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "6933d965-e4c4-4b49-bc99-08236b1d9458"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T20:18:50.871216+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "5d74eaed-dfb7-4095-beed-5ce1e6b5c522",
      "table_name": "PROJECT",
      "record_id": "ccfcfc03-d00a-4732-b8f7-99019000670b",
      "record_pk": {
        "id": "ccfcfc03-d00a-4732-b8f7-99019000670b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "ccfcfc03-d00a-4732-b8f7-99019000670b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "A real-time chat application powered by AI",
        "name": "AI Chat Application",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:06:24.593428+00:00"
      },
      "new_values": {
        "id": "ccfcfc03-d00a-4732-b8f7-99019000670b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "A real-time chat application powered by AI",
        "name": "AI Chat Application",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T06:06:24.593428+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T19:46:47.644609+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7d45f016-470d-46e6-8384-a19da816b796",
      "table_name": "PROJECT",
      "record_id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
      "record_pk": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
        "uid": "765bc84f-eba5-4d32-987b-d55adef7fe65",
        "desc": "tested to make it work, killed two views for this and it works",
        "name": "create to make sure default values work pls work",
        "members": [],
        "created_at": "2025-11-05T19:09:59.689236+00:00"
      },
      "new_values": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
        "uid": "765bc84f-eba5-4d32-987b-d55adef7fe65",
        "desc": "tested to make it work, killed two views for this and it works",
        "name": "create to make sure default values work pls work",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-11-05T19:09:59.689236+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T19:14:47.911213+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "b0c17bdb-1184-4772-b8d0-81f4d7a7239e",
      "table_name": "PROJECT",
      "record_id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
      "record_pk": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
        "uid": "765bc84f-eba5-4d32-987b-d55adef7fe65",
        "desc": null,
        "name": "create to make sure default values work pls work",
        "members": [],
        "created_at": "2025-11-05T19:09:59.689236+00:00"
      },
      "new_values": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
        "uid": "765bc84f-eba5-4d32-987b-d55adef7fe65",
        "desc": "tested to make it work, killed two views for this and it works",
        "name": "create to make sure default values work pls work",
        "members": [],
        "created_at": "2025-11-05T19:09:59.689236+00:00"
      },
      "changed_fields": [
        "desc"
      ],
      "delta": {
        "desc": {
          "new": "tested to make it work, killed two views for this and it works",
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T19:10:17.654019+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c5ad74e5-e237-4870-967d-b8e7ff589b26",
      "table_name": "PROJECT",
      "record_id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
      "record_pk": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "7824d5f4-3190-4df5-af81-9420ffcb54af",
        "uid": "765bc84f-eba5-4d32-987b-d55adef7fe65",
        "desc": null,
        "name": "create to make sure default values work pls work",
        "members": [],
        "created_at": "2025-11-05T19:09:59.689236+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-05T19:09:59.689236+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "49b46a7a-c94d-46c5-80bc-0ef6dd34863e",
      "table_name": "PROJECT",
      "record_id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
      "record_pk": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": [],
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "new_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T19:01:22.861405+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "075a0d87-8721-40ca-a3e5-c3905b09dad6",
      "table_name": "PROJECT",
      "record_id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
      "record_pk": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": null,
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "new_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": [],
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [],
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T18:59:32.570866+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "14b8fd3d-ef5e-4ce1-8cd7-6b438e0ea1f1",
      "table_name": "PROJECT",
      "record_id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
      "record_pk": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": [],
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "new_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": null,
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": null,
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T18:59:29.418117+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6c589cbe-ce40-4269-b059-f93bf6cabea3",
      "table_name": "PROJECT",
      "record_id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
      "record_pk": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": null,
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "new_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": [],
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [],
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T18:59:08.271506+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "aff61a19-2360-46d5-a4fa-76d7aef9fa24",
      "table_name": "PROJECT",
      "record_id": "352486e8-a727-470c-add4-10fe26f1fbce",
      "record_pk": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "17a40371-66fe-411a-963b-a977cc7cb475",
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "new_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "17a40371-66fe-411a-963b-a977cc7cb475",
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "6933d965-e4c4-4b49-bc99-08236b1d9458"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "17a40371-66fe-411a-963b-a977cc7cb475",
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "6933d965-e4c4-4b49-bc99-08236b1d9458"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "17a40371-66fe-411a-963b-a977cc7cb475",
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T18:31:55.3647+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "968a3afe-c40b-4b0a-9256-eb060e7dc2df",
      "table_name": "PROJECT",
      "record_id": "352486e8-a727-470c-add4-10fe26f1fbce",
      "record_pk": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "17a40371-66fe-411a-963b-a977cc7cb475",
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "new_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "17a40371-66fe-411a-963b-a977cc7cb475",
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "17a40371-66fe-411a-963b-a977cc7cb475",
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "17a40371-66fe-411a-963b-a977cc7cb475",
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-05T09:33:17.284358+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8b35d109-5307-4a84-be59-acb0becb5f90",
      "table_name": "PROJECT",
      "record_id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
      "record_pk": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND T^T",
        "members": [],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "new_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND T^T",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-11-04T21:31:31.052527+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "187246b7-36c7-4b3d-b092-47c1298ed0b2",
      "table_name": "PROJECT",
      "record_id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
      "record_pk": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "7f233f02-561e-4ada-9ecc-2f39320ee022",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING PLS DONT AMEND T^T",
        "members": [],
        "created_at": "2025-11-04T20:29:54.315946+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-04T20:29:54.315946+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e0e8f716-78f9-4a0b-953c-66990c2b9295",
      "table_name": "PROJECT",
      "record_id": "352486e8-a727-470c-add4-10fe26f1fbce",
      "record_pk": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "new_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "17a40371-66fe-411a-963b-a977cc7cb475",
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "bba910a9-1685-4fa3-af21-ccb2e11cf751"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "17a40371-66fe-411a-963b-a977cc7cb475",
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "bba910a9-1685-4fa3-af21-ccb2e11cf751"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "17a40371-66fe-411a-963b-a977cc7cb475"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-04T09:53:21.846129+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4f583b8c-7b9c-4e7b-8e17-ce23232af028",
      "table_name": "PROJECT",
      "record_id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
      "record_pk": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "desc manager test",
        "name": "manager test",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "da283ea9-552d-48dd-be56-18c81364adf0"
        ],
        "created_at": "2025-10-19T10:49:39.934347+00:00"
      },
      "new_values": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "desc manager test",
        "name": "manager test",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "da283ea9-552d-48dd-be56-18c81364adf0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-19T10:49:39.934347+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "da283ea9-552d-48dd-be56-18c81364adf0",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "da283ea9-552d-48dd-be56-18c81364adf0"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-11-04T07:50:40.887835+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "98a0022a-9f57-45d7-866d-876780236561",
      "table_name": "PROJECT",
      "record_id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
      "record_pk": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "desc manager test",
        "name": "manager test",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-19T10:49:39.934347+00:00"
      },
      "new_values": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "desc manager test",
        "name": "manager test",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "da283ea9-552d-48dd-be56-18c81364adf0"
        ],
        "created_at": "2025-10-19T10:49:39.934347+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "da283ea9-552d-48dd-be56-18c81364adf0"
          ],
          "old": [
            "944d73be-9625-4fd1-8c6a-00e161da0642"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-27T18:59:46.137305+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "cbcc86c9-28be-45e2-b6b0-fe10dda54f2f",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "944d73be-9625-4fd1-8c6a-00e161da0642"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-26T15:34:52.650364+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "228b1a5d-7243-4d14-a738-3caa46268146",
      "table_name": "PROJECT",
      "record_id": "695d5107-0229-481a-9301-7c0562ea52d1",
      "record_pk": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "new_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "944d73be-9625-4fd1-8c6a-00e161da0642"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-26T14:04:49.799466+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "70181f53-fe1b-4c75-b42f-ef4c0fa03038",
      "table_name": "PROJECT",
      "record_id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
      "record_pk": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": null,
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "new_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": null,
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "changed_fields": [
        "uid"
      ],
      "delta": {
        "uid": {
          "new": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "old": "655a9260-f871-480f-abea-ded735b2170a"
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T20:54:42.624935+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e029ab47-3695-46a5-ad75-b232bfa9aaa6",
      "table_name": "PROJECT",
      "record_id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
      "record_pk": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": null,
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "new_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": null,
        "created_at": "2025-10-13T12:35:02.56019+00:00"
      },
      "changed_fields": [
        "uid"
      ],
      "delta": {
        "uid": {
          "new": "655a9260-f871-480f-abea-ded735b2170a",
          "old": "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T20:54:08.23946+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f1f92553-d2c8-4eee-acfb-93cb1dbe1139",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00",
        "department": null
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00",
        "department": "HR"
      },
      "changed_fields": [
        "department"
      ],
      "delta": {
        "department": {
          "new": "HR",
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T10:23:05.395894+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0c64af3e-ad91-4477-93a7-51167987452a",
      "table_name": "PROJECT",
      "record_id": "ccfcfc03-d00a-4732-b8f7-99019000670b",
      "record_pk": {
        "id": "ccfcfc03-d00a-4732-b8f7-99019000670b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "ccfcfc03-d00a-4732-b8f7-99019000670b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "A real-time chat application powered by AI",
        "name": "AI Chat Application",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:06:24.593428+00:00",
        "department": null
      },
      "new_values": {
        "id": "ccfcfc03-d00a-4732-b8f7-99019000670b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "A real-time chat application powered by AI",
        "name": "AI Chat Application",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:06:24.593428+00:00",
        "department": "Tech"
      },
      "changed_fields": [
        "department"
      ],
      "delta": {
        "department": {
          "new": "Tech",
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T10:22:56.834417+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0d7ce5da-ccef-4251-b5fb-3616f8cdc39b",
      "table_name": "PROJECT",
      "record_id": "695d5107-0229-481a-9301-7c0562ea52d1",
      "record_pk": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00",
        "department": null
      },
      "new_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00",
        "department": "Quant"
      },
      "changed_fields": [
        "department"
      ],
      "delta": {
        "department": {
          "new": "Quant",
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T10:22:53.114071+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4c956b1e-7087-4255-b6e6-8768bf81d775",
      "table_name": "PROJECT",
      "record_id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
      "record_pk": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": null,
        "created_at": "2025-10-13T12:35:02.56019+00:00",
        "department": null
      },
      "new_values": {
        "id": "46c5da13-ca3a-44f3-ae9e-3cb7fd54f80b",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This function will send automated email to staff when their task due date is less than 24 hours away",
        "name": "Create email reminder functionality",
        "members": null,
        "created_at": "2025-10-13T12:35:02.56019+00:00",
        "department": "Quant"
      },
      "changed_fields": [
        "department"
      ],
      "delta": {
        "department": {
          "new": "Quant",
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T10:22:47.974453+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "1ac7262b-47e1-49b7-9b66-54043b8e8feb",
      "table_name": "PROJECT",
      "record_id": "352486e8-a727-470c-add4-10fe26f1fbce",
      "record_pk": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00",
        "department": null
      },
      "new_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00",
        "department": "Tech"
      },
      "changed_fields": [
        "department"
      ],
      "delta": {
        "department": {
          "new": "Tech",
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T10:22:43.490076+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d4d6ec17-d49f-49dc-8751-ad97a0ddb925",
      "table_name": "PROJECT",
      "record_id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
      "record_pk": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "desc manager test",
        "name": "manager test",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-19T10:49:39.934347+00:00",
        "department": null
      },
      "new_values": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "desc manager test",
        "name": "manager test",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-19T10:49:39.934347+00:00",
        "department": "Tech"
      },
      "changed_fields": [
        "department"
      ],
      "delta": {
        "department": {
          "new": "Tech",
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T10:22:18.193929+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "abacc697-a4e4-49ac-b8fd-36946e76fddb",
      "table_name": "PROJECT",
      "record_id": "352486e8-a727-470c-add4-10fe26f1fbce",
      "record_pk": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "new_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "17a40371-66fe-411a-963b-a977cc7cb475"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "944d73be-9625-4fd1-8c6a-00e161da0642"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T10:12:26.504099+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "215794ba-703e-4277-b5fe-587ce6e193b2",
      "table_name": "PROJECT",
      "record_id": "352486e8-a727-470c-add4-10fe26f1fbce",
      "record_pk": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "new_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "944d73be-9625-4fd1-8c6a-00e161da0642"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T10:11:44.615318+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c4002afb-62f1-43b4-80f0-f6bcc2bed523",
      "table_name": "PROJECT",
      "record_id": "352486e8-a727-470c-add4-10fe26f1fbce",
      "record_pk": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "new_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T10:04:21.880805+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "840b62ce-c436-408f-99ae-4aee9f81b625",
      "table_name": "PROJECT",
      "record_id": "352486e8-a727-470c-add4-10fe26f1fbce",
      "record_pk": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "352486e8-a727-470c-add4-10fe26f1fbce",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-25T10:03:48.066105+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-25T10:03:48.066105+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ae31e3c5-cca6-4815-a8b2-19dba315d802",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-25T10:03:11.37372+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "54564e7b-e815-4ecd-8b4a-70413ebbd0e7",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f",
            "17a40371-66fe-411a-963b-a977cc7cb475"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "17a40371-66fe-411a-963b-a977cc7cb475"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T09:08:35.211201+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f298aa8d-bdb1-4375-800f-e978d7c646c7",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "17a40371-66fe-411a-963b-a977cc7cb475"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "17a40371-66fe-411a-963b-a977cc7cb475"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f",
            "944d73be-9625-4fd1-8c6a-00e161da0642"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T08:59:23.581048+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4ef62888-9d6f-4220-a5bd-05fc1423ef76",
      "table_name": "PROJECT",
      "record_id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
      "record_pk": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "desc manager test",
        "name": "manager test",
        "members": null,
        "created_at": "2025-10-19T10:49:39.934347+00:00"
      },
      "new_values": {
        "id": "2c34dac5-b347-4b4f-aa41-a9e84030f39e",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "desc manager test",
        "name": "manager test",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-19T10:49:39.934347+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "944d73be-9625-4fd1-8c6a-00e161da0642"
          ],
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T08:58:40.801754+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a1f87f0f-435b-46fa-9b65-8439d9125c42",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f",
            "944d73be-9625-4fd1-8c6a-00e161da0642"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T08:57:06.423004+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "284bfb40-f64a-42c5-974b-643ae0a9d64f",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T07:28:19.441132+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "f0d97736-602e-4876-854a-c32b93795d55",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T07:07:04.679356+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e3ba818b-862f-4ec1-8c60-41dc124e60fc",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T07:06:44.243212+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e2a96845-31cb-4cd8-b2b7-f6c24dca1e00",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "944d73be-9625-4fd1-8c6a-00e161da0642"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "944d73be-9625-4fd1-8c6a-00e161da0642"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T07:03:41.990823+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ffef29bf-48ce-4487-90e0-e0ed3100d8dd",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T07:03:41.8556+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ad134378-084f-49bb-8654-2ae2daaacdb8",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T07:03:32.84895+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ec107b0d-c1ef-40bb-8363-dd396654c9e9",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:56:54.944864+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "42f76bd1-c710-48ba-b13b-16accb496a04",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:56:07.982692+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "bda338ee-7396-4864-8251-e8779f3caa64",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:56:07.887271+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "42aaa86a-dc7a-49e6-a642-b60df96fa70a",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:56:01.909556+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "437931d6-d87e-4bb2-95ef-3bb8861a2044",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:50:00.892242+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "bb00acee-ca77-4d98-aad0-91b5e5808c4c",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:50:00.804196+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "83b0dd1f-fc61-4887-953e-3cfbfaa4664d",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:49:12.305961+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d0233a60-f130-4d43-adc1-97c9bd51bdea",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:34:49.057919+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "09e37f87-b650-4274-89f0-7df2619a3e16",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:34:27.14594+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6b7fe44c-d3c9-4355-9416-a4b00da99943",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-10-25T06:33:38.0051+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0bafe13f-1d45-4159-a6e0-39f11cb998d7",
      "table_name": "PROJECT",
      "record_id": "26db0258-e3a3-4454-b921-f721c3f29283",
      "record_pk": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "26db0258-e3a3-4454-b921-f721c3f29283",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-25T06:19:00.78473+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-25T06:19:00.78473+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e6c51bc5-5783-4d61-afc7-e57c83f3e5c4",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-25T06:18:13.61245+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "98b17261-82ca-461b-9541-52459a5b17b1",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T09:34:48.282982+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8692530c-ad85-4a86-8586-3470a2ae3536",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T09:34:08.76065+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "eee1114a-ada0-438d-9a95-9684bad04edd",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T09:28:22.168418+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "61040c76-b384-4b4b-9dd1-bf4e020bc592",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T09:27:59.955333+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0e3b8255-b78e-4ec4-ae99-f83a3f55d267",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T09:10:51.540677+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "518cf8a4-1b8e-40d8-9aac-177bdec69d9f",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T09:09:26.549022+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7756ce50-5bdf-4883-bd8d-46f247eebb83",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "655a9260-f871-480f-abea-ded735b2170a",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "655a9260-f871-480f-abea-ded735b2170a",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T09:08:02.24136+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6185b714-76b6-4642-a05e-cb1e22900105",
      "table_name": "PROJECT",
      "record_id": "695d5107-0229-481a-9301-7c0562ea52d1",
      "record_pk": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "new_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:59:42.676442+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "3f2c4c40-f4c8-4016-b6e9-797936dd1c64",
      "table_name": "PROJECT",
      "record_id": "695d5107-0229-481a-9301-7c0562ea52d1",
      "record_pk": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "new_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:58:33.933226+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7eef01f7-3a96-4707-885e-db1a1f2442a1",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f",
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:58:30.8491+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "bb30f175-80d2-4462-a06a-c045fa292ea4",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "0ec8a99d-3aab-4ec6-b692-fda88656844f",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "0ec8a99d-3aab-4ec6-b692-fda88656844f",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:44:10.099803+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "08d1b435-cdf9-4765-8768-1f72b8bcba61",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:43:13.243006+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "75bbfabc-8bf1-4455-a3b6-e6fed668478e",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:31:20.93539+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "30d02981-2d05-4b5a-bab0-5c61839c2f2f",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:31:20.832882+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7c3a259b-9998-4a35-898b-3aa5e39c7f39",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:31:20.623136+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "da8843eb-ec65-4619-8b90-1412137f05a3",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:30:38.182751+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "4111cd27-c837-48c3-b5ca-d114191e695c",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:30:37.961982+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "81ee5684-c135-4b8f-9040-8e3ce593db33",
      "table_name": "PROJECT",
      "record_id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
      "record_pk": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "d1d2aa00-27ea-44a9-a81b-b218045395d0",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-24T08:28:49.780828+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-24T08:28:49.780828+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "660bd55e-84d7-4f2a-832d-bdd29d1b07db",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-24T08:27:13.237611+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "fa8a53d9-ab26-418b-8000-44c65205eed4",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:26:45.070475+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "81a5253a-ed8b-4c3a-a15c-cbe71687d880",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:20:39.665718+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c08b8245-c390-4f2b-b5cd-e1dcf1ea9ea5",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:20:39.545899+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9c54373a-152f-4dc1-b4f1-c78159f5fa81",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:14:26.908187+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "6d202d82-0e3c-4f05-9899-92c4c5f0b751",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:14:26.788734+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c6caa0fb-b487-4055-88fb-a9bac8c5a1a3",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:02:38.323912+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "b512bf35-0ece-4d2b-b768-fae14634a55f",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:02:38.153176+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "18a5261e-eb7a-4714-986f-6655a785cf32",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:02:37.940331+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "cf9029b1-516b-4bca-8f7d-dc6ca3f2650f",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:01:54.538343+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e8ade835-8dfc-4877-8804-a5efb7abfe9f",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T08:01:54.325595+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "18aa5f1a-8441-4eef-b926-43ad26b17693",
      "table_name": "PROJECT",
      "record_id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
      "record_pk": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "e2c9444b-71bd-45af-b983-9eea898e4b1c",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-24T08:01:09.100972+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-24T08:01:09.100972+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "160f75ad-5c9d-4527-859b-5858ef9d6ef2",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-24T07:57:34.550463+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "5f0bd450-5be4-4e8f-8ef8-8b9c3310db7d",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:43:37.100259+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "9c35b298-4bc9-45ff-a930-0d0a8bcff252",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:43:36.743074+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ef79093f-a55c-4ca3-9154-3b40f256b61e",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:43:36.471757+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "dd1166c6-483c-48b3-a3ac-4b06eba76a41",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:40:04.980007+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a3c92b79-ba8a-404f-801d-b6b578e3373e",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:32:52.521976+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7a07ed06-1d84-4927-ba93-46d6271fcb8d",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:32:52.177518+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "e9cee14b-beac-4192-a3a3-8934f08278bd",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:27:05.204077+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "67ed6ed0-4377-4f19-bb08-91f7364598ec",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:27:04.849312+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "201ed07a-045b-46eb-a53f-77e6d0196f52",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:27:04.651561+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7762c7ae-dd8d-4ab3-b50a-a729ba0d6ea9",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:25:48.920272+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a6a88ca5-1ba2-405a-9a88-b4995e09732f",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:25:48.724795+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7a1af9e6-dc2c-4d40-94f4-347d731a9913",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:10:28.916644+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "0cdc4681-5007-41a9-a4dc-810ee2051d9c",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:10:28.800474+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "8f6eb7f5-1286-4189-a8cb-d6eae7853ad7",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:10:28.660419+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "7ef9bf69-61a0-46d7-af28-c25d474ec03c",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:07:45.298172+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "a31db994-0969-451d-a07a-ca63c35ce6da",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T07:07:45.036251+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c0d439b8-0e99-4308-8c8d-8fe2f0111b97",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "0ec8a99d-3aab-4ec6-b692-fda88656844f"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "0ec8a99d-3aab-4ec6-b692-fda88656844f"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T06:56:32.836009+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "2c3b80db-28e9-430f-8c4c-03a3d19311d4",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T06:56:32.7139+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "553ce8ff-5b78-4228-a779-4662ade8af76",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T06:56:32.599916+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "ef5078e5-0327-403b-b38f-3a5e1e60a9b7",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T06:52:40.980792+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d80144f7-2c13-4935-aa0d-323c51023e73",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T06:52:40.871242+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "30b4544e-9cb9-4998-8d09-8165acf41a88",
      "table_name": "PROJECT",
      "record_id": "335cbc96-a931-48a1-9494-c92dd1f37410",
      "record_pk": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "335cbc96-a931-48a1-9494-c92dd1f37410",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "Xian xia",
        "name": "Delete this project",
        "members": [],
        "created_at": "2025-10-24T06:50:29.708994+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-24T06:50:29.708994+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "710d1834-08dd-41f8-980d-766376df9786",
      "table_name": "PROJECT",
      "record_id": "695d5107-0229-481a-9301-7c0562ea52d1",
      "record_pk": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "new_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
          ],
          "old": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T06:38:06.080216+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "07633d89-e030-4e49-af9d-fff9621153f7",
      "table_name": "PROJECT",
      "record_id": "695d5107-0229-481a-9301-7c0562ea52d1",
      "record_pk": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "new_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a"
          ],
          "old": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ]
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T06:38:05.842995+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "1b78f4fc-775c-406d-917a-798d517f20da",
      "table_name": "PROJECT",
      "record_id": "695d5107-0229-481a-9301-7c0562ea52d1",
      "record_pk": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": null,
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "new_values": {
        "id": "695d5107-0229-481a-9301-7c0562ea52d1",
        "uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "desc": "This project aims to recreate the authenthication, to make the app more secure",
        "name": "Revamp Authenthication",
        "members": [
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-10T05:06:38.602368+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T06:38:05.605428+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "c8be0f31-cdbf-460d-b7ca-a549ecc1426f",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": null,
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e"
          ],
          "old": null
        }
      },
      "user_id": null,
      "timestamp": "2025-10-24T06:07:08.961793+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "fe31a10a-94e3-4ed9-9d81-a3e68530e6c9",
      "table_name": "PROJECT",
      "record_id": "ccfcfc03-d00a-4732-b8f7-99019000670b",
      "record_pk": {
        "id": "ccfcfc03-d00a-4732-b8f7-99019000670b"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "ccfcfc03-d00a-4732-b8f7-99019000670b",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "A real-time chat application powered by AI",
        "name": "AI Chat Application",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e"
        ],
        "created_at": "2025-10-24T06:06:24.593428+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-24T06:06:24.593428+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "b9b21362-f77a-4ee9-b637-143dd5fa098d",
      "table_name": "PROJECT",
      "record_id": "9e9ebc69-fb45-4ba1-87ed-da177b182bf6",
      "record_pk": {
        "id": "9e9ebc69-fb45-4ba1-87ed-da177b182bf6"
      },
      "operation": "DELETE",
      "old_values": {
        "id": "9e9ebc69-fb45-4ba1-87ed-da177b182bf6",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "A real-time chat application powered by AI",
        "name": "AI Chat Application",
        "members": null,
        "created_at": "2025-10-24T05:57:04.421828+00:00"
      },
      "new_values": null,
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-24T06:06:18.647345+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "77582dae-dd2d-4d93-a4e2-2f698efbb790",
      "table_name": "PROJECT",
      "record_id": "9e9ebc69-fb45-4ba1-87ed-da177b182bf6",
      "record_pk": {
        "id": "9e9ebc69-fb45-4ba1-87ed-da177b182bf6"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "9e9ebc69-fb45-4ba1-87ed-da177b182bf6",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "A real-time chat application powered by AI",
        "name": "AI Chat Application",
        "members": null,
        "created_at": "2025-10-24T05:57:04.421828+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-24T05:57:04.421828+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "d686bae7-bbba-41ed-87be-1801573ae6cc",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "test",
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "testname",
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": [
        "name"
      ],
      "delta": {
        "name": {
          "new": "testname",
          "old": "test"
        }
      },
      "user_id": null,
      "timestamp": "2025-10-23T11:04:53.386963+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "28570e34-2282-41d5-9552-2c349f81b954",
      "table_name": "PROJECT",
      "record_id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "record_pk": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "f434f31d-3c12-4867-889c-794edf0c6199",
        "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "desc": "testing audit trail",
        "name": "test",
        "created_at": "2025-10-23T11:03:47.431495+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-10-23T11:03:47.431495+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    }
  ]
}
```

### Get logs by project ID

GET http://localhost:5200/logs/{pid}

> http://localhost:5200/logs/2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a

Sample Output:

```json
{
  "message": "Log retrieved successfully",
  "log": [
    {
      "id": "bb9d02f1-4895-4ff7-a316-52d7062a535a",
      "table_name": "PROJECT",
      "record_id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
      "record_pk": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a"
      },
      "operation": "UPDATE",
      "old_values": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING JW CY DONT AMEND",
        "members": [],
        "created_at": "2025-11-06T22:07:01.818074+00:00"
      },
      "new_values": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING JW CY DONT AMEND",
        "members": [
          "655a9260-f871-480f-abea-ded735b2170a",
          "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
          "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
          "944d73be-9625-4fd1-8c6a-00e161da0642",
          "fb892a63-2401-46fc-b660-bf3fe1196d4e",
          "6933d965-e4c4-4b49-bc99-08236b1d9458"
        ],
        "created_at": "2025-11-06T22:07:01.818074+00:00"
      },
      "changed_fields": [
        "members"
      ],
      "delta": {
        "members": {
          "new": [
            "655a9260-f871-480f-abea-ded735b2170a",
            "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            "a43815c3-2051-44b9-9646-8ceaf9d6cb87",
            "944d73be-9625-4fd1-8c6a-00e161da0642",
            "fb892a63-2401-46fc-b660-bf3fe1196d4e",
            "6933d965-e4c4-4b49-bc99-08236b1d9458"
          ],
          "old": []
        }
      },
      "user_id": null,
      "timestamp": "2025-11-06T22:46:33.478295+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    },
    {
      "id": "02c2b435-76cc-40d8-ab91-2e5f26896995",
      "table_name": "PROJECT",
      "record_id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
      "record_pk": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a"
      },
      "operation": "INSERT",
      "old_values": null,
      "new_values": {
        "id": "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a",
        "uid": "655a9260-f871-480f-abea-ded735b2170a",
        "desc": "bros i cant find the btn",
        "name": "TESTING JW CY DONT AMEND",
        "members": [],
        "created_at": "2025-11-06T22:07:01.818074+00:00"
      },
      "changed_fields": null,
      "delta": null,
      "user_id": null,
      "timestamp": "2025-11-06T22:07:01.818074+00:00",
      "ip_address": null,
      "user_agent": null,
      "session_id": null
    }
  ]
}
```

### Get projects by department

GET http://localhost:5200/department/{department}

> http://localhost:5200/department/HR

Sample Output:

```json
{
  "message": "3 project(s) retrieved",
  "projects": [
    {
      "id": "f434f31d-3c12-4867-889c-794edf0c6199",
      "uid": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
      "created_at": "2025-10-23T11:03:47.431495+00:00",
      "name": "testname",
      "desc": "testing audit trail",
      "members": [
        "944d73be-9625-4fd1-8c6a-00e161da0642",
        "fb892a63-2401-46fc-b660-bf3fe1196d4e",
        "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "bba910a9-1685-4fa3-af21-ccb2e11cf751",
        "0ec8a99d-3aab-4ec6-b692-fda88656844f"
      ],
      "department": "HR"
    },
    {
      "id": "1ebfba1a-afa0-4bc0-9cc3-1bfd0f7acad7",
      "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "created_at": "2025-11-07T01:29:40.480486+00:00",
      "name": "itest-all-1",
      "desc": null,
      "members": [],
      "department": "HR"
    },
    {
      "id": "2644b4c6-61e1-48d2-9531-1df42142b3f7",
      "uid": "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
      "created_at": "2025-11-07T01:29:40.816691+00:00",
      "name": "itest-all-2",
      "desc": null,
      "members": [],
      "department": "HR"
    }
  ]
}
```
