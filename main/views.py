from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Follow, Notification, PrivateMessage, Category, Tag 
from .forms import  CommentForm, MessageForm, PostForm, EditPostForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Count

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.views += 1
    post.save()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to comment.")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'form': form,
    })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post.id)

def home(request):
    top_posts = (
        Post.objects.filter(image__isnull=False, is_draft=False)
        .annotate(like_count=Count('likes'))
        .order_by('-like_count')[:4]
    )
    posts_with_images = Post.objects.filter(image__isnull=False, is_draft=False).exclude(image='').order_by('-created_at')
    posts_without_images = Post.objects.filter(Q(image__isnull=True) | Q(image='')).order_by('-created_at')
    
    context = {
        'top_posts': top_posts,
        'posts_with_images': posts_with_images,
        'posts_without_images': posts_without_images,
    }
    return render(request, 'home.html', context)

def filter_posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category, is_draft=False).order_by('-created_at')
    categories = Category.objects.all()  # Fetch categories for use in the template
    return render(request, 'category_posts.html', {
        'category': category,
        'posts': posts,
        'categories': categories,
    })
   
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query), is_draft=False
    )
    return render(request, 'search_results.html', {'posts': posts, 'query': query})

@login_required
def post_analytics(request):
    posts = request.user.posts.annotate(
        like_count=Count('likes'),
        comment_count=Count('comments')
    ).order_by('-created_at')

    return render(request, 'post_analytics.html', {'posts': posts})

@login_required
def private_messages(request):
    received_messages = request.user.received_messages.all()
    sent_messages = request.user.sent_messages.all()
    return render(request, 'private_messages.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('private_messages')
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form, 'receiver': receiver})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = user.posts.filter(is_draft=False).order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'user_profile.html', {
        'user': user,
        'posts': posts,
        'is_following': is_following,
    })

def author_profile(request, author_id):
    author = get_object_or_404(User, id=author_id)
    posts = author.posts.filter(is_draft=False).order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, following=author).exists()
    return render(request, 'author_profile.html', {
        'author': author,
        'posts': posts,
        'is_following': is_following,
    })

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)  # Redirect to the post detail view
    else:
        form = EditPostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'delete_post.html', {'post': post})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow == request.user:
        messages.error(request, "You cannot follow yourself.")
    else:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        messages.success(request, f"You are now following {user_to_follow.username}.")
    return redirect('author_profile', author_id=user_to_follow.id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow_instance = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
    if follow_instance.exists():
        follow_instance.delete()
        messages.success(request, f"You have unfollowed {user_to_unfollow.username}.")
    else:
        messages.error(request, "You are not following this user.")
    return redirect('author_profile', author_id=user_to_unfollow.id)

@login_required
def following_list(request):
    following = request.user.following.all()
    return render(request, 'following_list.html', {'following': following})

@login_required
def followers_list(request):
    followers = request.user.followers.all()
    return render(request, 'followers_list.html', {'followers': followers})


