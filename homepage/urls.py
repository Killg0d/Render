from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('base', views.home, name='home'),
    path('test', views.test, name='test'),
    path('admin', views.admin, name='admin'),
    path('about', views.about, name='about'),
    path('blog', views.blog, name='blog'),
    path('contact', views.contact, name='contact'),
    path('job_details', views.job_details, name='job_details'),
    path('job_details/<int:job_id>/', views.job_details, name='job_details'),
    path('job_listing', views.job_listing, name='job_listing'),
    path('single_blog', views.single_blog, name='single_blog'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    path('jobs/<int:category_id>', views.get_jobs_by_category,
         name='get_jobs_by_category'),
    path('single_blog/<int:blog_id>/', views.single_blog, name='single_blog'),
    path('add_comment/<int:blog_id>/', views.add_comment, name='add_comment'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('admin/logout/', views.custom_logout, name='admin_logout'),

]
