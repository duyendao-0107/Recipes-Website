from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = ( ('draft', 'Draft'), ('published', 'Published'), )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_posts')
    body = models.TextField()
    image = models.ImageField(upload_to='posts/image/%Y/%m/%d/', blank=True)
    video = models.FileField(upload_to='posts/video/%Y/%m/%d/', blank=True)
    url = models.URLField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    score = models.IntegerField(default=0, 
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
    
    class Meta:
        ordering = ('-publish',)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipe:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
    def get_absolute_url_home(self):
        return reverse('recipe:post_detail_home', args=[ self.slug, self.publish.year, self.publish.month, self.publish.day])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
