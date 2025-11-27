from django.urls import path, register_converter
from blog.views import *



class MultilingualSlugConverter:
    # پشتیبانی از: حروف انگلیسی، فارسی، اعداد، خط تیره و زیرخط
    regex = '[-\w\u0600-\u06FF]+'
    
    def to_python(self, value):
        return value
    
    def to_url(self, value):
        return value

register_converter(MultilingualSlugConverter, 'mslug')



app_name='blog'
urlpatterns = [
    path('', blog_view,name='home'),
    path('search/',blog_search,name='search'),
    path('tag/<mslug:tag_name>/', blog_tag, name='tag'),
    path('<mslug:slug>/', blog_single,name='single'),
    path('category/<str:cat_name>',blog_category,name='category'),
    path('author/<str:author_username>',blog_view,name='author'),
    path('search/',blog_search,name='search'),

]