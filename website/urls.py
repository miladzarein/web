from django.urls import path
from website.views import *

urlpatterns = [
    path('', home_view,name='home'),
    path('about/', about_view,name='about'),
    path('contact/', contact_view,name='contact'),
    path('newsletter/', newsletter_view,name='newsletter'),

]