from django import forms
from django import forms
from .models import Post, Document, Contact, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')
        
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'document')
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'




class Subscribe(forms.Form):
    Email = forms.EmailField()
    
    # def __str__(self):
    #     return self.Email
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')