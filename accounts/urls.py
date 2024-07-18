from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path('', latest_blog_posts, name='latest_blog_posts'),
    path('register/', registerPage, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('logout/', logoutUser, name='logout'),
    path('post/create/', create_post, name='create_post'),
    path('post/edit/<int:pk>/', edit_post, name='edit_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
