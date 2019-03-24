from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from . models import Post, Comment
from django.contrib.auth import login, logout, authenticate
from . forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'cover']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'cover']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('blogapp:post-index')


class CommentCreateView(CreateView):
    model = Comment
    fields = ['comment']

    def get_absolute_url(self):
        return reverse('blogapp:post-detail', args=[str(self.pk)])

    def form_valid(self, form, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['comment']

    def form_valid(self, form, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('blogapp:post-index')


def signup(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('blogapp:post-index')
    return render(request, 'registration/signup.html', {'form': form})
