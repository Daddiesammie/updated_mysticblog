# admin.py
from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import SiteSettings

class SiteSettingsAdminForm(forms.ModelForm):
    about_us = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    disclaimer = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    privacy_policy = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    terms_and_conditions = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    cookies_policy = forms.CharField(widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = SiteSettings
        fields = '__all__'

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsAdminForm
    fieldsets = (
        ('Site Logo', {
            'fields': ('logo',),
        }),
        ('Site Content', {
            'fields': ('about_us', 'disclaimer', 'privacy_policy', 
                      'terms_and_conditions', 'cookies_policy'),
            'classes': ('full-width',)
        }),
        ('Social Media Links', {
            'fields': ('telegram', 'instagram', 'github', 'twitter', 'facebook'),
        }),
    )

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'ckeditor/ckeditor-init.js',
            'ckeditor/ckeditor/ckeditor.js',
        )
        css = {
            'all': ('admin/css/forms.css',)
        }

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False