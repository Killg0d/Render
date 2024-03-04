from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Categories, Blog, Comment, Feedback
from users.models import Company, JobProvider
from jobpost.models import Job
from django.contrib.auth.models import User, auth
from django.contrib import messages
import mysql.connector as sql
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F
# Create your views here.
from django.db.models import Subquery, OuterRef
from django.core.paginator import Paginator

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from django.contrib.auth import logout


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        messages.success(request, 'Thankyou for Subscribing')
    return redirect(reverse('index'))


def custom_logout(request):
    logout(request)
    # Redirect to your preferred login URL
    return redirect(reverse('index'))


@require_GET
def get_jobs_by_category(request, category_id):
    jobs = Job.objects.filter(category_id=category_id)
    job_data = []
    for job in jobs:
        job_data.append({
            'img': job.job_provider.company.image.url,
            'title': job.title,
            'category': job.category.category_name,
            'country': job.country.name,
            'salary': job.salary,
            'post_date': job.post_date,
        })
    print(job_data)
    return JsonResponse({'jobs': job_data})


def index(request):

    job_provider_id = Job.objects.values(
        'job_provider_id').distinct().values_list('job_provider_id', flat=True)
    jobs = []
    for job in job_provider_id:
        job = Job.objects.filter(job_provider_id=job).first()
        if job:
            jobs.append(job)
            if len(jobs) == 4:  # Fetch only four jobs
                break

    print(list(jobs))
    cats = Categories.objects.all()
    blog_posts = Blog.objects.all()[:2]
    params = {
        'cats': cats,
        'jobs': jobs,
        'blog_posts': blog_posts
    }
    return render(request, 'index.html', params)


def home(request):
    return render(request, 'base.html')


def admin(request):
    admin_url = reverse('admin:index')
    return redirect(admin_url)


def test(request):
    return render(request, 'profile.html')


def about(request):
    feedbacks = Feedback.objects.all()  # Retrieve all feedback instances
    rating_range = range(1, 6)  # Set the rating range from 1 to 5
    print(rating_range)
    context = {
        'feedbacks': feedbacks,
        'rating_range': rating_range,
    }
    return render(request, 'about.html', context)


def blog(request):
    blog_posts = Blog.objects.all()
    paginator = Paginator(blog_posts, 4)  # Show 10 blog posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blogs': page_obj,
        'paginator': paginator,
    }
    return render(request, 'blog.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        send_email(request, subject=subject, message=message, toemail=email)

    return render(request, 'contact.html')


def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        pass

    params = {
        'job': job
    }
    return render(request, 'job_details.html', params)


def job_listing(request):
    jobs = Job.objects.order_by('id')
    cats = Categories.objects.all()
    user_id = request.user.id

    # Set the number of jobs to display per page
    jobs_per_page = 10
    selected_category = request.GET.get('select')
    if selected_category:
        jobs = jobs.filter(category=selected_category)
    # Create a Paginator object with the jobs queryset and the desired number of jobs per page
    paginator = Paginator(jobs, jobs_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page object from the Paginator
    page_obj = paginator.get_page(page_number)

    if user_id:
        job_providers = JobProvider.objects.filter(user_id=user_id)
        if job_providers.exists():
            job_provider = job_providers.first()
            company = job_provider.company
            if company:
                company_image = company.image.url
            else:
                company_image = None
        else:
            company_image = None
    else:
        company_image = None
    print(company_image)
    print(selected_category)
    params = {
        'jobs': page_obj,
        'cats': cats,
        'paginator': paginator,
        'selected_category': selected_category,
    }
    return render(request, 'job_listing.html', params)


def single_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = Comment.objects.filter(blog=blog)
    previous_blog = Blog.objects.filter(id__lt=blog_id).order_by('-id').first()
    next_blog = Blog.objects.filter(id__gt=blog_id).order_by('id').first()
    params = {
        'blog': blog,
        'comments': comments,
        'next_blog': next_blog,
        'previous_blog': previous_blog
    }
    return render(request, 'single_blog.html', params)


def add_comment(request, blog_id):
    if request.method == 'POST':
        # Get the comment data from the request
        comment_text = request.POST.get('comment')
        blog = Blog.objects.get(id=blog_id)
        user = request.user

        # Create a new comment object
        comment = Comment.objects.create(
            blog=blog,
            author=user,
            content=comment_text
        )

        # Redirect to the blog detail page or any other desired page
        return redirect('single_blog', blog_id=blog_id)


def send_email(request, subject, message, toemail):
    try:
        print(toemail)
        send_mail(subject, message+' '+toemail, None, [
            'jobproindia90@gmail.com'], fail_silently=False)
        messages.success(request, 'Email sent successfully!')
    except Exception as e:
        messages.error(request, f'Error sending email: {str(e)}')

    return redirect('contact')


@login_required(login_url='login')
def feedback_view(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        if request.user.is_authenticated:
            user_feedback = Feedback.objects.filter(user=request.user).first()
            if user_feedback and user_feedback.given:
                messages.info(request, 'You have already provided feedback.')
                return redirect('job_listing')
            else:
                feedback = Feedback.objects.create(
                    user=request.user, rating=rating, message=message, given=True)
                messages.success(request, 'Thank you for providing feedback.')
                # Redirect to the appropriate page after feedback submission
                return redirect('job_listing')
        else:
            messages.warning(
                request, 'You need to be logged in to provide feedback.')
            # Redirect to the login page if user is not logged in
            return redirect('login')

    return render(request, 'feedback.html')
