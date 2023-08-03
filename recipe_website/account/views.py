from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from recipe.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from images.models import Image

def home(request):
    object_list = Post.published.all()
    
    images = Image.objects.all()
    
    paginator = Paginator(object_list, 6)
    
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
        
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'account/home.html', {'section': 'home', 
                                                 'posts': posts, 
                                                 'images': images})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password( user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            
            # Create the user profile
            Profile.objects.create(user=new_user)
            
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
            
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid ():
            user_form.save()
            
            profile_form.save()

            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        
        profile_form = ProfileEditForm(instance=request.user.profile)
            
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})