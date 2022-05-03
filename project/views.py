from django.contrib.auth import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from project.models import Post
from django.contrib.auth.models import User
from .forms import AddNewPost, AddProfile
from django.views.decorators.csrf import csrf_exempt

def index(request):
    latest_posts = Post.objects.all().order_by('-date')
    return render(request, 'project/index.html', {'latest_posts': latest_posts})

def profile_view(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        profileForm = AddProfile(request.POST, instance=user.profile)
        if profileForm.is_valid():
            profileForm.save()
            return redirect('project:profile', username=request.user)
    else:
        addProfileForm = AddProfile(instance=user.profile)
        return render(request, 'project/profile.html', {'user': user, 'addProfileForm': addProfileForm})

@login_required
def add_new_post(request):
    if request.method == 'POST':
        form = AddNewPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.poster = request.user
            post.save()
            return redirect('project:index')
    else:
        form = AddNewPost()
    return render(request, 'project/add_new_post.html', {'form': form})


def edit_video(request, video_id):
    return HttpResponse("You're editing video %s." % video_id)


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project:index')
    else:
        form = forms.UserCreationForm()
    return render(request, 'project/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('project:index')
    else:
        form = AuthenticationForm()
    return render(request, 'project/login.html', {'form': form})
