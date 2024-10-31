from django import forms
from .models import Comment, BlogPost, Tag
from ckeditor_uploader.widgets import CKEditorUploadingWidget
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none'}),
        }

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'featured_image', 'categories', 'tags', 'is_published']