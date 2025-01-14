from django import forms
from .models import Post, Comment, PrivateMessage, Category,Tag
from django_ckeditor_5.fields import CKEditor5Widget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']
        category = forms.ModelChoiceField(queryset=Category.objects.all())
        tags = forms.ModelChoiceField(queryset=Tag.objects.all())
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'content': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}),
            'category':forms.Select(attrs={'class': 'form-control w-100'}),
            'image':forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
class MessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class':"form-control w-100"})
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tag']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Post Title'
            }),
            'content': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tag': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
        }