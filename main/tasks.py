# main/tasks.py

import logging
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from mebel_app.celery import app
from django.core.mail import send_mail
from django.conf import settings

# Task to send the letters from users to Manager

@app.task
def send_verification_email(txt,user_email):
    send_mail(
        'Это просто тест',
        txt,
        settings.APP_EMAIL,
        [user_email],
        fail_silently=False,
    )
