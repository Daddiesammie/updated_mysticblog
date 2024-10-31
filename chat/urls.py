# urls.py
from django.urls import path
from . import views
from django.http import HttpResponse

app_name = 'chat'

def test_view(request):
    return HttpResponse("Chat app is working!")

urlpatterns = [
    path('', views.chatroom_redirect, name='chatroom_redirect'),
    path('list/', views.chatroom_list, name='chatroom_list'),
    path('room/<int:room_id>/', views.chatroom_detail, name='chatroom_detail'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
]