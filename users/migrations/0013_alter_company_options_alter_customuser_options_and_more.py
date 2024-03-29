# Generated by Django 4.2 on 2023-05-27 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_remove_jobseeker_country_remove_jobseeker_dob_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'managed': True, 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'managed': True, 'verbose_name': 'ModelName', 'verbose_name_plural': 'ModelNames'},
        ),
        migrations.AlterModelOptions(
            name='jobprovider',
            options={'managed': True, 'verbose_name': 'JobProvider', 'verbose_name_plural': 'JobProviders'},
        ),
        migrations.AlterModelTable(
            name='company',
            table='Company',
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='Users',
        ),
        migrations.AlterModelTable(
            name='jobprovider',
            table='JobProvider',
        ),
    ]
