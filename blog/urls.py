from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='post_list'),
    path('search/', views.BlogPostSearchView.as_view(), name='search'),
    path('rss/', LatestPostsFeed(), name='rss_feed'),
    path('<slug:slug>/', views.BlogPostDetailView.as_view(), name='post_detail'),
    path('tag/<slug:tag_slug>/', views.BlogPostListView.as_view(), name='post_list_by_tag'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('exclusive/', views.ExclusivePostListView.as_view(), name='exclusive_post_list'),
]