from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CommentForm, PostCreateForm
from images.models import Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

def post_list(request):
    posts = Post.published.all()
    
    return render(request, 'recipe/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, 
                             status='published', 
                             publish__year=year, 
                             publish__month=month, 
                             publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    return render(request, 'recipe/post/detail.html', {'post': post,
                                                       'comments': comments, 
                                                       'new_comment': new_comment, 
                                                       'comment_form': comment_form})

@login_required
def post_create(request):
    if request.method == 'POST':
        
        post_form = PostCreateForm(data=request.POST, files=request.FILES)
        
        if post_form.is_valid ():
            post_form.save()

            messages.success(request, 'Post updated successfully')
            return HttpResponseRedirect("/menu/")
        else:
            messages.error(request, 'Error updating your profile')
       
    else:
        post_form = PostCreateForm(data=request.GET)
            
    return render(request, 'recipe/post/create.html', {'post_form': post_form})
