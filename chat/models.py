from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatRoom(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    participants = models.ManyToManyField(User, related_name='chatrooms', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mentioned_users = models.ManyToManyField(User, related_name='mentions', blank=True)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'

    def save(self, *args, **kwargs):
        if self.pk:
            self.is_edited = True
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('mention', 'Mention'),
        ('new_message', 'New Message'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.notification_type} notification for {self.recipient.username}'

    class Meta:
        ordering = ['-created_at']