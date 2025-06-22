from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.models import Client, Message, Newsletter


def home(requests):
    return render(requests, 'mailing/home.html')


# Clients
class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client


# Message
class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message


#  Newsletter
class NewsletterListView(ListView):
    model = Newsletter


class NewsletterDetailView(DetailView):
    model = Newsletter


class NewsletterCreateView(CreateView):
    model = Newsletter


class NewsletterUpdateView(UpdateView):
    model = Newsletter


class NewsletterDeleteView(DeleteView):
    model = Newsletter
