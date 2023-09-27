from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from django.utils import timezone
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('afterlogin')
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                error_message = "Username is already taken."
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})
            
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})


@login_required
def afterlogin(request):
    posts = Post.objects.all().order_by('-pub_date')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('afterlogin')  # Redirect to the blog page after creating a post
    else:
        form = PostForm()
    return render(request, 'afterlogin.html', {'posts': posts, 'form': form})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('afterlogin')
    else:
        form = PostForm()
    return render(request, 'afterlogin.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'afterlogin.html', {'post': post})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Check if the user is the author of the post
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                edited_post = form.save(commit=False)
                edited_post.edit_date = timezone.now()  # Set the edit date to the current time
                edited_post.save()
                return redirect('afterlogin')
        else:
            form = PostForm(instance=post)
        return render(request, 'edit_post.html', {'form': form, 'post': post})
    else:
        # Handle the case where the user is not the author of the post
        return render(request, 'edit_post_error.html')
    

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Ensure that only the author of the post can delete it
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('afterlogin')
        return render(request, 'delete_confirm.html', {'post': post})
    else:
        return render(request, 'delete_post_error.html')