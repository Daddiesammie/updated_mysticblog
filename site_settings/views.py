from django.shortcuts import render
from .models import SiteSettings

def your_view(request):
    site_settings = SiteSettings.load()  # Load the SiteSettings instance
    return render(request, 'your_template.html', {'site_settings': site_settings})

def disclaimer_view(request):
    settings = SiteSettings.load()
    return render(request, 'site_settings/disclaimer.html', {'settings': settings})

def about_us_view(request):
    settings = SiteSettings.load()
    return render(request, 'site_settings/about_us.html', {'settings': settings})

def privacy_policy_view(request):
    settings = SiteSettings.load()
    return render(request, 'site_settings/privacy_policy.html', {'settings': settings})

def terms_and_conditions_view(request):
    settings = SiteSettings.load()
    return render(request, 'site_settings/terms_and_conditions.html', {'settings': settings})

def cookies_policy_view(request):
    settings = SiteSettings.load()
    return render(request, 'site_settings/cookies_policy.html', {'settings': settings})


