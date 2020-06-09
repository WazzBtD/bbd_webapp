from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Topic, Post
from .forms import TopicCreateForm, PostCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

login_req = login_required(login_url='/login')


@login_req
def topic_create(request):
    if request.method == 'POST':
        form = TopicCreateForm(data=request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            messages.success(request, f"Utworzono nowy temat!")
            return redirect('forum:topic-detail', topic.id)
        else:
            messages.error(request, f"Nie udało się utworzyć nowego tematu.")
    return render(request=request,
                  template_name="forum/topic_form.html",
                  context={"form": TopicCreateForm()})


@login_req
def post_create(request, topic_id):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.forum_topic = Topic.objects.get(pk=topic_id)
            post.save()
            messages.success(request, f"Utworzono nowy post!")
            return redirect('forum:topic-detail', topic_id)
        else:
            messages.error(request, f"Nie udało się utworzyć nowego postu.")
    return render(request=request,
                  template_name="forum/post_form.html",
                  context={"form": PostCreateForm()})


@method_decorator(login_req,  name='dispatch')
class TopicList(ListView):

    model = Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_req,  name='dispatch')
class TopicDetail(DetailView):

    model = Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(forum_topic=self.kwargs['pk'])
        return context