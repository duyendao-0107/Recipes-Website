from django.urls import path
from . import views
import account

app_name = 'recipe' 

urlpatterns = [ 
    # post views
    path('your-post-list/', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<slug:post>/<int:year>/<int:month>/<int:day>/', views.post_detail_home, name='post_detail_home'),
    path('rate/', views.rate_post, name='rate_post'),
    path('ranking/', views.post_ranking, name='ranking'),
]