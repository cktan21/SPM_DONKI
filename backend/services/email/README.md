# Email Service 📧

A lightweight Python service for sending emails via SMTP.  
Currently, the service runs as a script and automatically sends an email when executed.

---

## 🚀 Current Stage
This project is a **work in progress** and will be modified and integrated in future sprints.  
At this stage, it demonstrates basic email sending functionality.

---

## 🛠️ How to Run

### Using Docker

cd into the email folder then run the docker code

```bash
docker build -t email .
docker run --env-file .env email
```
Currently, running the above code would spin up a new container and send a email automatically
In future stages, this should not be a container by itself, and should not send out email automatically.

## How it Works:

To try sending a email to yourself, modify the receiver_email argument passed in to the 
send_email function in main.py and run the docker command

```bash
send_email(receiver_email, subject, body)
send_email("as354ri6ff@zudpck.com", "Reminder!", "Your task is due in 24 hours 🚨")


