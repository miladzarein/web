from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post


class BlogSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return Post.objects.filter(status=True)
    
    def lastmod(self, obj):
        return  obj.published_date
    
    def location(self, obj):
        return reverse('blog:single', kwargs={'slug': obj.slug})