from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from newsletter.views import newsletter_signup

urlpatterns = [
    path('admin/', include('django_admin_kubi.urls')),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')), 
    path('', include('blog.urls')),
    path('users/', include('users.urls')),
    path('profiles/profile/', include('profiles.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('newsletter/signup/', newsletter_signup, name='newsletter_signup'),
    path('newsletter/', include('newsletter.urls', namespace='newsletter')),
    path('site-settings/', include('site_settings.urls')),
     # Ensure this line is present and correct
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)