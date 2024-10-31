from django.urls import path
from . import views
from .views import your_view 

app_name = 'site_settings'

urlpatterns = [
    path('disclaimer/', views.disclaimer_view, name='disclaimer'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions_view, name='terms_and_conditions'),
    path('cookies-policy/', views.cookies_policy_view, name='cookies_policy'),
    path('about_us/', views.about_us_view, name='about_us'),
    path('connect/', your_view, name='connect'),
]