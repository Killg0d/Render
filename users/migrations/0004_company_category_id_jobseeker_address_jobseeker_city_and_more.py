# Generated by Django 4.2 on 2023-05-19 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
        ('users', '0003_company_jobprovider'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='category_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='homepage.categories'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='education',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='profile_img',
            field=models.ImageField(default='profiles/profile.png', upload_to=''),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='skills',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='work_experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]
