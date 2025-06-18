from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, approve_post, reject_post

urlpatterns = [
    path('', PostListView.as_view(), name="blog-home"),
    path('post-new/', PostCreateView.as_view(), name="blog-new"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="blog-delete"),
    path('post/<int:pk>/approve/', approve_post, name='approve-post'),  # Add this line
    path('post/<int:pk>/reject/', reject_post, name='reject-post'),    # Add this line
    path('about/', views.about, name="blog-about"),
]
