# Generated by Django 4.2 on 2023-05-26 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category_heading',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
