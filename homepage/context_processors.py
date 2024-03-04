from users.models import JobProvider, Jobseeker
from jobpost.models import Notification


def notification_count(request):
    # Get the count of unread notifications
    user = request.user
    unread_count = None
    if user.is_authenticated:
        unread_count = Notification.objects.filter(
            user=request.user, is_read=False).count()
        # Return the count as a dictionary
    return {'unread_count': unread_count}


def user_image(request):
    user = request.user
    profile_image = None

    if user.is_authenticated:
        if user.user_type == 'Job Seeker':
            jobseeker = Jobseeker.objects.get(username_id=user.id)
            if jobseeker.profile_img:
                profile_image = jobseeker.profile_img.url
        elif user.user_type == 'Job Provider':
            job_provider = JobProvider.objects.filter(user=user).first()
            if job_provider and job_provider.company:
                profile_image = job_provider.company.image.url

    return {'user_image': profile_image}
