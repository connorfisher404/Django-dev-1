from django import forms
from .models import Comment, UserProfile, Post, ChatMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3})
        }


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'bio', 'relationship_status']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']


class FollowForm(forms.Form):
    follow = forms.BooleanField(initial=False, required=False)



class MessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']