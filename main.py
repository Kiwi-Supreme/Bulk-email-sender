from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import asyncio
from send_email import send_email
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Load email list once
with open("email_list.json", "r") as f:
    email_list = json.load(f)["emails"]

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/send", response_class=HTMLResponse)
async def send_bulk_email(
    request: Request,
    subject: str = Form(...),
    message: str = Form(...)
):
    tasks = []
    for email in email_list:
        tasks.append(send_email(email, subject, message))
        
    await asyncio.gather(*tasks)
    return templates.TemplateResponse("success.html", {
        "request": request,
        "subject": subject,
        "message": message
    })
