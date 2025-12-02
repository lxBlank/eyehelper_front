from django.urls import path, include
from rest_framework.routers import DefaultRouter
from message import views



urlpatterns = [
    path('setMessage/', views.MessageViewSet.as_view({'post': 'createMessage'})),
    path('getMessage/', views.MessageViewSet.as_view({'get': 'getMessage'})),
    path('getAllMessage/', views.MessageViewSet.as_view({'get': 'getAllMessage'})),
]