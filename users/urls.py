from django.urls import path, include

app_name = 'users'

urlpatters = [
    path('',include('django.contrib.auth.urls')),
]