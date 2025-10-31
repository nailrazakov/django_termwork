from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.models import Client, Message, Newsletter, Attempt
from mailing.forms import MessageForm, ClientForm, NewsletterForm
from mailing.services import send_newsletter


def home(requests):
    return render(requests, 'mailing/main.html')


class AttemptListView(ListView):
    model = Attempt
    context_object_name = 'attempts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.has_perm("sender.can_view_attempt_mailing"):
            attempts_list = Attempt.objects.all()
        else:
            attempts_list = [
                attempt
                for attempt in Attempt.objects.all()
                if attempt.owner == user
            ]

        context.update(
            {
                "attempts_list": attempts_list,
                "successfully_attempts": [
                    attempt
                    for attempt in attempts_list
                    if attempt.status == "success"
                ],
                "unsuccessfully_attempts": [
                    attempt
                    for attempt in attempts_list
                    if attempt.status == "failed"
                ],
            }
        )
        return context


# Clients
class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")


# Message
class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


#  Newsletter
class NewsletterListView(ListView):
    model = Newsletter


class NewsletterDetailView(DetailView):
    model = Newsletter


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailing:newsletter_list")

    def form_valid(self, form):
        print(form)
        send_newsletter('nail-razakov@yandex.ru')
        return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailing:newsletter_list")


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy("mailing:newsletter_list")
