from django.contrib import admin
from blog.models import Post,Category,Comment

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('title','counted_views','status','published_date','created_date')
    list_filter = ('status',)
    search_fields = ['title','content']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','subject','approved','created_date')
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    search_fields = ['name','email','subject']
    list_filter = ('name','post')

