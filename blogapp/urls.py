from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('', views.PostListView.as_view(), name='post-index'),
    path('<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('create-post', views.PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/update-post', views.PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete-post', views.PostDeleteView.as_view(), name='post-delete'),
    path('<int:pk>/add-comment', views.CommentCreateView.as_view(), name='comment-create'),
    path('<int:pk>/update-comment', views.CommentUpdateView.as_view(), name='comment-update'),
    path('<int:pk>/delete-comment', views.CommentDeleteView.as_view(), name='comment-delete'),
]
