# chat/admin.py
from django.contrib import admin
from .models import ChatRoom, Message, Notification

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'chatroom', 'content', 'created_at', 'is_edited')
    list_filter = ('chatroom', 'created_at', 'is_edited')
    search_fields = ('content', 'user__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username',)