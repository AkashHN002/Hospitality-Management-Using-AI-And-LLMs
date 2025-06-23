import requests
import json


import smtplib
from email.message import EmailMessage
import ssl
import os
import time



Webhook_URL = os.getenv("WEBHOOK")


def send_email(sender_email, sender_password, receiver_email, subject, body):
    
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as sm:
            sm.login(sender_email, sender_password)
            sm.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        
def send_alert(message):
    slack_data = {
        'text': message
    }
    response = requests.post(
        Webhook_URL, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
    
