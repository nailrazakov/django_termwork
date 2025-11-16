from django import forms
from .models import Client, Newsletter, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'fio', 'phone', 'tg_nik', 'comment']


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['follow_up', 'periodicity', 'status', 'clients', 'message', 'owner']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
