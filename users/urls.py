from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, email_verification, UserListView, UserDetailView, UserUpdateView, UserDeleteView
from django.conf.urls.static import static
from django.conf import settings

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailing:home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/email-confirm/<str:token>/', email_verification, name='email_confirm'),

    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
