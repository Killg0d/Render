# Generated by Django 4.2 on 2023-06-02 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_customuser_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='category_id',
        ),
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(default='profiles/profile.png', upload_to='company_images/'),
        ),
    ]