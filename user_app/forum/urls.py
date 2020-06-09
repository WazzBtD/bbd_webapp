from django.urls import path

from . import views

urlpatterns = [
    path('topic', views.topic_create, name='topic-create'),
    path('topic/<int:topic_id>/post', views.post_create, name='post-create'),
    path('', views.TopicList.as_view(), name='topic-list'),
    path('topic/<int:pk>', views.TopicDetail.as_view(), name='topic-detail'),
]