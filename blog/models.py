from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import re
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
 

def create_persian_slug(text):
    """
    ایجاد اسلاگ خودکار از تایتل برای فارسی و انگلیسی
    """
    # تبدیل اعداد فارسی به انگلیسی
    persian_numbers = '۰۱۲۳۴۵۶۷۸۹'
    english_numbers = '0123456789'
    translation_table = str.maketrans(persian_numbers, english_numbers)
    text = text.translate(translation_table)
    
    # حذف کاراکترهای غیرمجاز و جایگزینی فضاها با خط تیره
    text = re.sub(r'[^\w\s\u0600-\u06FF-]', '', text)
    text = re.sub(r'[\s]+', '-', text.strip())
    return text






class Post(models.Model):
    image = models.ImageField(upload_to='blog/', default='blog/default.jpg')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = TaggableManager()
    category = models.ManyToManyField(Category)
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=200, allow_unicode=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            # ایجاد اسلاگ برای فارسی و انگلیسی
            self.slug = create_persian_slug(self.title)


            # جلوگیری از اسلاگ تکراری
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)



    class Meta:
        ordering = ['-created_date']


    def __str__(self):
        return self.title
    

    def snippets (self):
        return self.content[:100]
    



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return self.name