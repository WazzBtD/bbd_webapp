from .models import Topic, Post
from django.forms import ModelForm


class TopicCreateForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title']


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text']
