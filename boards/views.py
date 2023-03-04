from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count

from django.views.generic import CreateView, UpdateView

from django.urls import reverse_lazy

# Create your views here.
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards':boards})
    

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    
    if request.method == 'POST':
        user = request.user
        form = NewTopicForm(request.POST)
        
        if form.is_valid():
            topic = form.save(commit=False)
            
            topic.board = board
            topic.starter = user
            topic.save()
        
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = user,
                update_by = user
            )
        
            return redirect('topic_post', pk=pk, topic_pk=topic.pk)
    
    else:
        form = NewTopicForm()
    
    print(form.errors)
    
    return render(request, 'new_topic.html', {'board':board, 'form':form})


def topic_post(request, pk, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk, board__pk=pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_post.html', {'topic':topic})


@login_required
def reply_post(request, pk, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk, board__pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_post', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    
    return render(request, 'reply_topic.html', {'topic':topic, 'form':form})

# class ReplyPostView(CreateView):
#     model = Post
#     form_class = PostForm
#     success_url = reverse_lazy('topic_post')
#     template_name = 'new_post.html'
    
    # def get_topic(self, board_pk, topic_pk):
    #     self.topic = get_object_or_404(Topic, pk=topic_pk, board__pk=board_pk)
        
    # def _render(self, request):
    #     return render(request, 'reply_topic.html', {'topic':self.topic, 'form':self.form})
    
    # def get(self, request, pk, topic_pk):
    #     self.get_topic(pk, topic_pk)
    #     self.form = PostForm()
    #     return self._render(request)
    
    # def post(self, request, pk, topic_pk):
    #     self.get_topic(pk, topic_pk)
    #     self.form = PostForm(request.POST)
    #     if self.form.is_valid():
    #         post = self.form.save(commit=False)
    #         post.topic = self.topic
    #         post.created_by = request.user
    #         post.save()
    #         return redirect('topic_post', pk=pk, topic_pk=topic_pk)
    #     return self._render(request)
    

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.save()
        return redirect('topic_post', pk=post.topic.board.pk, topic_pk=post.topic.pk)