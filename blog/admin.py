from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'status')
    list_filter = ('status', 'author')
    search_fields = ('title', 'content')
    actions = ['approve_posts', 'reject_posts']

    def approve_posts(self, request, queryset):
        queryset.update(status='A')
    approve_posts.short_description = 'Approve selected posts'

    def reject_posts(self, request, queryset):
        queryset.update(status='R')
    reject_posts.short_description = 'Reject selected posts'

admin.site.register(Post, PostAdmin)
