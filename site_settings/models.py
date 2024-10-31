# models.py
from django.db import models
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField

class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='site_settings/', null=True, blank=True)
    about_us = RichTextUploadingField(blank=True)
    disclaimer = RichTextUploadingField(blank=True)
    privacy_policy = RichTextUploadingField(blank=True)
    terms_and_conditions = RichTextUploadingField(blank=True)
    cookies_policy = RichTextUploadingField(blank=True)
    telegram = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)

    def clean(self):
        if SiteSettings.objects.exists() and not self.pk:
            raise ValidationError("There can only be one SiteSettings instance")

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SiteSettings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"