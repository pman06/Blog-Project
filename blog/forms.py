from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body','tags', 'slug','image']

        widgets = {
            'title' : forms.TextInput(attrs={'class':'textinputclass form-control'}),
            'body' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent form-control'}),
            'tags': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class':'form-control-file'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author','text']

        widgets = {
            'author' : forms.TextInput(attrs={'class':'textinputclass form-control'}),
            'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent form-control'})
        }

class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =[]

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    to_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
