from celery import shared_task
from django.core.mail import send_mail


@shared_task
def hello():
    from_email = 'aleksei.tchetvyorkin@yandex.ru'
    send_mail(subject='subject', message='sefsefsef', from_email=from_email, recipient_list=['kexaxa4@gmail.com'],
              html_message='message')
