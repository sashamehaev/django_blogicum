from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('edit_profile/<slug:username>/', views.edit_profile, name="edit_profile"),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('blog/create_post/', views.index, name='create_post'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
]
