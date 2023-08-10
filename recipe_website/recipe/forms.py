from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'author', 'body', 'image', 'video', 'status', 
                  'servings', 'ingredients', 'direction_step', 'nutrition_calories', 
                  'nutrition_carbs', 'nutrition_protein', 'nutrition_fat')

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'author', 'body', 'image', 'video', 'status', 
                  'servings', 'ingredients', 'direction_step', 'nutrition_calories', 
                  'nutrition_carbs', 'nutrition_protein', 'nutrition_fat')
