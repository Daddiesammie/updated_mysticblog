from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import BlogPost, Comment, Like, Tag, Category
from .forms import CommentForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

class ExclusivePostListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/exclusive_post_list.html'
    context_object_name = 'exclusive_posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True, is_exclusive=True).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    post_list = BlogPost.objects.filter(categories=category, is_published=True).order_by('-published_at')
    
    paginator = Paginator(post_list, 9)  # Show 9 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts,
        'is_paginated': posts.has_other_pages(),
        'page_obj': posts
    })

@require_POST
@csrf_protect
def newsletter_signup(request):
    email = request.POST.get('email')
    # Here you would typically save this email to your database or send it to your email service provider
    # For now, we'll just return a success message
    return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing!'})

@require_POST
@login_required
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # User has already liked this post, so unlike it
        like.delete()
        liked = False
    else:
        liked = True
    
    likes_count = post.likes.count()
    
    return JsonResponse({
        'liked': liked,
        'likes_count': likes_count
    })

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True, is_exclusive=False).order_by('-published_at')
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exclusive_posts'] = BlogPost.objects.filter(is_published=True, is_exclusive=True).order_by('-published_at')[:5]
        return context

class BlogPostDetailView(FormMixin, DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['likes_count'] = self.object.likes.count()
        context['tags'] = self.object.tags.all()
        if self.request.user.is_authenticated:
            context['user_has_liked'] = self.object.likes.filter(user=self.request.user).exists()
        
        context['meta_description'] = self.object.content[:160] + '...' if len(self.object.content) > 160 else self.object.content
        context['og_title'] = self.object.title
        context['og_description'] = context['meta_description']
        if self.object.featured_image:
            context['og_image'] = self.request.build_absolute_uri(self.object.featured_image.url)
        
        # Fetch recommended posts (posts with the same tags)
        context['recommended_posts'] = BlogPost.objects.filter(tags__in=self.object.tags.all()).exclude(id=self.object.id).distinct()[:3]
        
        return context

        
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
    
class BlogPostSearchView(ListView):
    model = BlogPost
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return BlogPost.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(categories__name__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct().order_by('-published_at')
        return BlogPost.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context