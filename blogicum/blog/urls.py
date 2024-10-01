from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<slug:username>/', views.UserDetailView.as_view(), name='profile'),
    path('blog/create_post/', views.index, name='create_post'),
    path('blog/edit_profile/', views.index, name='edit_profile'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
]
