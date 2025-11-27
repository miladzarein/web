from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .forms import ContactForm,NewsletterForm
from django.contrib import messages
from blog.models import Post

def home_view(request):
    # دریافت آخرین پست‌های بلاگ
    posts = Post.objects.filter(status=1).order_by('-published_date')[:4]  # 3 پست آخر
    context = {
        'posts': posts  # ارسال پست‌ها به تمپلیت
    }
    return render(request, 'website/home.html', context)

def about_view(request):
    return render(request, 'website/about.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد!")
        else:
            messages.error(request,"مشکلی پیش آمده مجددا تلاش کنید")
        return redirect('/contact')
    else:
        form = ContactForm()
    return render(request, 'website/contact.html', {'form': form})



def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "آدرس ایمیل با موفقیت ثبت شد!")
        else:
            messages.error(request, "ایمیل وارد شده معتبر نیست!")
        return redirect('/') 
