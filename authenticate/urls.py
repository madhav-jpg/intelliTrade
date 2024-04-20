from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.signin, name='signin'),
    path('dashboard/', include('dashboard.urls')),
]