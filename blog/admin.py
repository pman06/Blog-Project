from django.contrib import admin

from .models import Post, Comment
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_date')
    list_filter = ('created_date','published_date','author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy ='published_date'
    ordering = ('published_date',)
#admin.site.register(Post)
#admin.site.register(Comment)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display= ('author', 'post', 'text', 'created_date', 'approved_comment' )
    list_filter = ('approved_comment', 'created_date')
    search_fields = ('author','text')
