from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Categories, Job, JobProvider, JobApply, Notification
from django.contrib.auth.models import User, auth
from django.contrib import messages
import mysql.connector as sql
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
# Create your views here.


def editjob(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.category_id = request.POST.get('category')
        job.description = request.POST.get('description')
        job.salary = request.POST.get('salary')
        job.skills = request.POST.get('skills')
        job.end_date = request.POST.get('enddate')
        job.country = request.POST.get('country')
        job.education = request.POST.get('education')
        job.save()
        messages.success(request, 'Changes successful')
        print('user created')
        return redirect('alljobs')

        # Redirect to a success page or perform any additional actions
    else:
        print('Unsuccessful')
    print(job)
   # Render the template
    cats = Categories.objects.all()
    params = {
        'cats': cats,
        'job': job
    }
    return render(request, 'jobpost/editjob.html', params)


def providerdash(request):
    return render(request, 'jobpost/providerdash.html')


def providerhome(request):
    if request.method == 'POST':
        pass

    if request.user.user_type == 'Job Provider':
        provider = JobProvider.objects.filter(user=request.user.id)
        params = {
            'provider': provider
        }
    return render(request, 'jobpost/provider_home.html', params)


@login_required
def alljobs(request):

    user_id = request.user.id
    if user_id:
        jobs = Job.objects.filter(job_provider__user_id=user_id)
    else:
        jobs = Job.objects.none()
    print(jobs)
    numbers = range(1, len(jobs) + 1)
    # Perform further operations with the category_name
    params = {'jobs': jobs, 'numbers': numbers}
    return render(request, 'jobpost/alljobs.html', params)


def createjob(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        salary = request.POST.get('salary')
        skills = request.POST.get('skills')
        enddate = request.POST.get('enddate')
        country = request.POST.get('country')
        education = request.POST.get('education')
        job_provider = JobProvider.objects.get(user=request.user)
        category = Categories.objects.get(category_id=category_id)
        # Create a new job post object and save it to the database.
        job = Job(
            title=title,
            category=category,
            description=description,
            salary=salary,
            skills=skills,
            end_date=enddate,
            country=country,
            education=education,
            job_provider=job_provider
        )
        job.save()

        # Redirect the user to the job post list page.
        return redirect('alljobs')
    cats = Categories.objects.all()
    params = {
        'cats': cats}
    return render(request, 'jobpost/createjob.html', params)


def applications(request):
    if request.user.user_type == 'Job Provider':

        applications = JobApply.objects.filter(
            job_provider__user=request.user.id, status=None)
        numbers = range(1, len(applications) + 1)

        params = {
            'applications': applications, 'numbers': numbers
        }

    return render(request, 'jobpost/applications.html', params)


def acceptedjob(request):
    if request.user.user_type == 'Job Provider':

        applications = JobApply.objects.filter(
            job_provider__user=request.user.id, status=1)

        params = {
            'applications': applications,
        }
    return render(request, 'jobpost/acceptedjob.html', params)


def acceptedjobwithid(request, application_id):
    application = get_object_or_404(JobApply, id=application_id)
    create_notification(user=application.job_seeker.username,
                        message=f'You have been selected for the job of {application.job.title} in {application.job_provider.company.name}')
    # Update the status of the application to 1
    application.status = 1
    application.save()

    return redirect('acceptedjob')


def rejectedjob(request):
    if request.user.user_type == 'Job Provider':

        applications = JobApply.objects.filter(
            job_provider__user=request.user.id, status=0)

        params = {
            'applications': applications,
        }
    return render(request, 'jobpost/rejectedjob.html', params)


def rejectedjobwithid(request, application_id):
    application = get_object_or_404(JobApply, id=application_id)

    # Update the status of the application to 1
    application.status = 0
    application.save()
    create_notification(user=application.job_seeker.username,
                        message=f'You have been rejected for the job of {application.job.title} in {application.job_provider.company.name}')
    return redirect('rejectedjob')


def deleteapplicationwithid(request, application_id):
    application = get_object_or_404(JobApply, id=application_id)

    # Update the status of the application to 1

    application.delete()
    return redirect('applications')


def delete_job(request, job_id):
    # Retrieve the job instance based on the job_id
    job = get_object_or_404(Job, id=job_id)

    # Perform the deletion
    job.delete()

    # Redirect the user to a relevant page after the deletion (e.g., job list page)
    return redirect('alljobs')


def apply_view(request, job_id):
    # Get the job object based on the job_id parameter
    job = get_object_or_404(Job, id=job_id)

    if request.user.is_authenticated and request.user.user_type == 'Job Seeker':
        job_seeker = request.user.jobseeker

        try:
            # Check if the job seeker has already applied for this job
            job_apply = JobApply.objects.get(job=job, job_seeker=job_seeker)
            messages.warning(request, 'Already applied')
            print('Already applied')
        except JobApply.DoesNotExist:
            # Create a job application for the job seeker and job
            JobApply.objects.create(
                job_provider=job.job_provider, job_seeker=job_seeker, job=job)
            messages.success(request, 'Application submitted successfully')
            print('Application submitted successfully')
            create_notification(
                job.job_provider.user, f'An Application has been submited for the post of {job.title}')

    else:
        messages.warning(request, 'Please log in')
        print('Login required')
        return redirect('login')

    return redirect('job_listing')


def applicant_view(request):
    return render(request, 'jobpost/applicant_view.html')


def create_notification(user, message):
    notification = Notification(user=user, message=message)
    notification.save()


@login_required
def show_notification(request):
    user = request.user
    notifications = Notification.objects.filter(
        user=user, is_read=False).order_by('-created_at')

    context = {
        'notifications': notifications
    }

    return render(request, 'notification.html', context)


def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('show_notification')


def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    notification.delete()
    return redirect('show_notification')


def send_offer(request, application_id):
    application = get_object_or_404(JobApply, id=application_id)

    if request.method == 'POST':
        try:
            file = request.FILES.get('file')
            if file.content_type != 'application/pdf':
                raise ValueError(
                    'Invalid file type. Only PDF files are allowed.')

            subject = f'Job Offer Letter for {application.job_provider.company.name}'
            message = f'Please find attached the job offer letter for the post of {application.job.title}.'
            from_email = application.job_provider.user.email
            to_email = [application.job_seeker.username.email]

            email = EmailMessage(subject, message, from_email, to_email)
            # Attach the offer letter file
            email.attach(file.name, file.read(), 'application/pdf')
            email.send()
            messages.success(request, 'Offer letter sent')
        except Exception as e:
            messages.error(request, f'Error in sending: {str(e)}')
        return redirect('acceptedjob')

    return redirect('acceptedjob')
