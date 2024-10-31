from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatRoom, Message, Notification
from django.core.paginator import Paginator
from .forms import MessageForm

@login_required
def chatroom_redirect(request):
    print("Chatroom redirect view called")
    chatroom = ChatRoom.objects.filter(is_active=True).first()
    if not chatroom:
        chatroom = ChatRoom.objects.create(
            title="General Discussion",
            description="Welcome to our chat!",
            created_by=request.user
        )
    return redirect('chat:chatroom_detail', room_id=chatroom.id)

@login_required
def chatroom_list(request):
    chatrooms = ChatRoom.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'chat/chatroom_list.html', {'chatrooms': chatrooms})

@login_required
def chatroom_detail(request, room_id):
    chatroom = get_object_or_404(ChatRoom, id=room_id, is_active=True)
    messages = Message.objects.filter(chatroom=chatroom).order_by('created_at')[:50]

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chatroom = chatroom
            message.user = request.user
            message.save()
            return redirect('chat:chatroom_detail', room_id=room_id)
    else:
        form = MessageForm()

    return render(request, 'chat/chatroom_detail.html', {
        'chatroom': chatroom,
        'messages': messages,
        'form': form
    })

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)
    message.delete()
    return JsonResponse({'status': 'success'})

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        message.content = content
        message.save()
        return JsonResponse({'status': 'success', 'content': content})
    return JsonResponse({'status': 'error'}, status=400)

