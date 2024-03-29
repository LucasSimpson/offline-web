from django.urls import path

from . import views

app_name = 'index'
urlpatterns = [
    path('', views.HomeView.as_view()),
    path('proxy/<path:proxy_url>', views.ProxyView.as_view()),
]
