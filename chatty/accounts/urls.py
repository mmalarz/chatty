from django.contrib.auth.views import LoginView, logout
from django.urls import path

from accounts.views import registration, settings

app_name = 'accounts'

urlpatterns = [
    path('registration', registration, name='registration'),
    path('login', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout', logout, name='logout'),
    path('<slug:current_user>/settings', settings, name='settings')
]
