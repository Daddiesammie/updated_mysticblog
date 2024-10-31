from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, BlogPost, Comment, Like, Tag

class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorUploadingWidget(),
        required=True
    )
    
    class Meta:
        model = BlogPost
        fields = '__all__'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'author', 'is_published', 'is_exclusive', 'published_at')
    list_filter = ('is_published', 'is_exclusive', 'categories', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    filter_horizontal = ('categories', 'tags')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('full-width',)  # This helps with editor width
        }),
        ('Media', {
            'fields': ('featured_image',),
        }),
        ('Categorization', {
            'fields': ('categories', 'tags'),
        }),
        ('Publication', {
            'fields': ('author', 'is_published', 'is_exclusive', 'published_at'),
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
    
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',  # jQuery
            'ckeditor/ckeditor-init.js',  # CKEditor initialization
            'ckeditor/ckeditor/ckeditor.js',  # CKEditor main script
        )
        css = {
            'all': ('admin/css/forms.css',)
        }

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author__username', 'content', 'post__title')
    actions = ['approve_comments', 'unapprove_comments']
    readonly_fields = ('created_at', 'updated_at')

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments were successfully approved.')
    approve_comments.short_description = "Approve selected comments"

    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments were successfully unapproved.')
    unapprove_comments.short_description = "Unapprove selected comments"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')
    readonly_fields = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_posts_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def get_posts_count(self, obj):
        return obj.posts.count()
    get_posts_count.short_description = 'Posts Count'