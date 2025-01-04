from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import PasswordChangingForm
from django.contrib.auth.models import User
from main.models import Follow
from django.contrib.auth.decorators import login_required
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from main.models import UserProfile
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home') 

def signup_view(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username:
            errors['username'] = "Username is required."
        elif User.objects.filter(username=username).exists():
            errors['username'] = "This username is already taken."

        if not email:
            errors['email'] = "Email is required."
        elif User.objects.filter(email=email).exists():
            errors['email'] = "This email is already registered."

        if not password1:
            errors['password1'] = "Password is required."
        elif len(password1) < 6:
            errors['password1'] = "Password must be at least 6 characters long."

        if password1 != password2:
            errors['password2'] = "Passwords do not match."

        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')

    return render(request, 'registration/signup.html', {'errors': errors})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = user.posts.filter(is_draft=False)
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'registration/user_profile.html', {
        'user': user,
        'posts': posts,
        'is_following': is_following,
    })

def validate_url(url):
    """Validate URL or return None for invalid URLs."""
    if url:
        url_validator = URLValidator()
        try:
            url_validator(url)
            return url
        except ValidationError:
            return None
    return None

@login_required
def update_profile(request):
    """View to handle updating user profile."""
    # Ensure profile exists
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Update User fields
        request.user.first_name = request.POST.get("first_name", "").strip()
        request.user.last_name = request.POST.get("last_name", "").strip()

        # Validate URL fields
        instagram = validate_url(request.POST.get("instagram", "").strip())
        youtube = validate_url(request.POST.get("youtube", "").strip())
        facebook = validate_url(request.POST.get("facebook", "").strip())
        x = validate_url(request.POST.get("x", "").strip())

        if not all([request.POST.get("instagram", "").strip() == instagram,
                    request.POST.get("youtube", "").strip() == youtube,
                    request.POST.get("facebook", "").strip() == facebook,
                    request.POST.get("x", "").strip() == x]):
            messages.warning(request, "Some URLs provided are invalid and were ignored.")

        # Update UserProfile fields
        profile.bio = request.POST.get("bio", "").strip()
        profile.instagram = instagram
        profile.youtube = youtube
        profile.facebook = facebook
        profile.x = x

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        try:
            # Save user and profile updates
            request.user.save()
            profile.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect(reverse('user_profile', kwargs={'user_id': request.user.id}))
        except Exception as e:
            messages.error(request, f"An error occurred while updating your profile: {str(e)}")
            return render(request, 'registration/update_profile.html', {'profile': profile})

    return render(request, 'registration/update_profile.html', {'profile': profile})

class PasswordChange(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'registration/password_success.html', {})

def author_followers_view(request, author_id):
    author = get_object_or_404(User, id=author_id)
    followers = author.profile.followers.all()  
    return render(request, 'registration/author_followers.html', {
        'author': author,
        'followers': followers,
    })

def author_following_view(request, author_id):
    author = get_object_or_404(User, id=author_id)
    following = author.profile.following.all()  
    return render(request, 'registration/author_following.html', {
        'author': author,
        'following': following,
    })
