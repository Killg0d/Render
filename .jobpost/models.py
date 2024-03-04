from django.db import models
from homepage.models import Categories
from users.models import JobProvider, Jobseeker, CustomUser
from django_countries.fields import CountryField
from django.utils import timezone
STATUS_CHOICES = (
    (None, 'Pending'),
    (1, 'Accepted'),
    (0, 'Rejected'),
)


class Job(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    skills = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    country = CountryField()
    education = models.TextField()
    job_provider = models.ForeignKey(JobProvider, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Jobs'
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return f"Job Provided By {self.job_provider.user.username} for {self.title}"
    def delete_if_expired(self):
        if self.end_date < timezone.now().date():
            self.delete()

class JobApply(models.Model):
    job_provider = models.ForeignKey(JobProvider, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(Jobseeker, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    apply_date = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        # Define a unique constraint to ensure a job seeker can apply for a job only once
        unique_together = ('job_seeker', 'job')
        db_table = 'Applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return f"Job Application for {self.job.title}"


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'Notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"Notification for {self.user} as {self.message}"
