from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body','tags', 'image']

        widgets = {
            'title' : forms.TextInput(attrs={'class':'textinputclass', 'rows':'30', 'cols':'4'}),
            'body' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})

        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author','text']

        widgets = {
            'author' : forms.TextInput(attrs={'class':'textinputclass'}),
            'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =[]
