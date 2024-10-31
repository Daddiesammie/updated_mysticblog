from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserForm
from blog.models import Comment, Like

@login_required
def profile_view(request):
    # Get recent comments by the user - using 'author' instead of 'user'
    comments = Comment.objects.filter(
        author=request.user
    ).select_related('post').order_by('-created_at')[:5]  # Get 5 most recent comments
    
    # Get recent likes by the user (assuming you have the Like model set up)
    likes = Like.objects.filter(
        user=request.user
    ).select_related('post').order_by('-created_at')[:5]  # Get 5 most recent likes
    
    context = {
        'comments': comments,
        'likes': likes,
    }
    
    return render(request, 'profiles/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profiles:profile')  # Changed this line to include namespace
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })