from django.contrib import admin

# Register your models here.
from .models import BlogPost, Comment, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author')
    list_filter  = ('created', 'updated')
    search_fields = ('author__username', 'title')
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy  = ('created')


admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
