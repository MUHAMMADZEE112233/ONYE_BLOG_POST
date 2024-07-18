from django.contrib import admin
from .models import CustomUser, Post, Category

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Category)
