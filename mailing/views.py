from smtplib import SMTPException

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from config.settings import EMAIL_HOST_USER
from mailing.models import Client, Message, Newsletter, Attempt
from mailing.forms import MessageForm, ClientForm, NewsletterForm
from mailing.services import send_newsletter
from django.core.mail import send_mail


def home(requests):
    total_mailings = Attempt.objects.count()
    active_mailings = Attempt.objects.filter(status='successfully').count()
    unique_clients = Client.objects.values('email').distinct().count()
    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
    }
    return render(requests, 'mailing/main.html', context)


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
                    if attempt.status == "successfully"
                ],
                "unsuccessfully_attempts": [
                    attempt
                    for attempt in attempts_list
                    if attempt.status == "unsuccessfully"
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


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailing:newsletter_list")


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy("mailing:newsletter_list")


class MailingSendAttemptView(LoginRequiredMixin, View):
    def get(self, request, pk):
        newsletter = get_object_or_404(Newsletter, pk=pk)
        return render(request, template_name='mailing/main.html')

    def post(self, request, pk, *args, **kwargs):
        newsletter = get_object_or_404(Newsletter, pk=pk)
        if newsletter and newsletter.status == 'created' or newsletter.status == 'launched':
            clients = newsletter.clients.all()
            for client in clients:
                try:
                    send_mail(newsletter.message.subject, newsletter.message.body, EMAIL_HOST_USER, [client.email])
                    Attempt.objects.create(mailing=newsletter,
                                           status="successfully",
                                           server_response="Сообщение отправлено успешно",
                                           owner=request.user
                                           )
                except SMTPException as e:
                    Attempt.objects.create(mailing=newsletter,
                                           status="unsuccessfully",
                                           server_response=str(e),
                                           owner=request.user)
        newsletter.status = "launched"
        newsletter.save()
        return redirect("mailing:attempt_list")


