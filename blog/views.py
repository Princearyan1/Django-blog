from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]

    def get_queryset(self):
        # Include both approved and pending posts
        return Post.objects.all().order_by('-date_posted')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_queryset(self):
        # Include both approved and pending posts
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.status == 'P':
            context['pending_message'] = "This post is pending approval and is not yet visible to the public."
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'P'  # Set the status to 'Pending'
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'P'  # Reset status to 'Pending' on update
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# New view functions for approval and rejection
def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_superuser:
        post.status = 'A'  # Assuming 'A' means approved
        post.save()
    return redirect('blog-detail', pk=post.pk)

def reject_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_superuser:
        post.status = 'R'  # Assuming 'R' means rejected
        post.save()
    return redirect('blog-detail', pk=post.pk)
