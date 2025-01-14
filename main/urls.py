from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('search/', views.search_posts, name='search_posts'),
    path('messages/', views.private_messages, name='private_messages'),
    path('post/',views.post_detail, name='post_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('author/<int:author_id>/', views.author_profile, name='author_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('following/', views.following_list, name='following_list'),
    path('followers/', views.followers_list, name='followers_list'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('analytics/', views.post_analytics, name='post_analytics'),
    path('category/<int:category_id>/', views.filter_posts_by_category, name='filter_posts_by_category'),
    path('add-category/', views.add_category, name='add_category'),
    path('category-dropdown/', views.posts_by_category, name='posts_by_category'),
    path('tag/<slug:slug>/', views.posts_by_tag, name='posts_by_tag')
]

