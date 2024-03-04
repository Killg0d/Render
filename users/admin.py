
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *
from PIL import Image
from django.forms import ModelChoiceField
from django import forms


class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.user_type.lower() == 'job provider' and not hasattr(obj, 'Job Provider'):
            job_provider = JobProvider(user=obj)
            job_provider.save()

        if obj.user_type.lower() == 'job seeker' and not hasattr(obj, 'Job Seeker'):
            job_seeker = Jobseeker(username=obj, email=obj.email, first_name=obj.first_name,
                                   last_name=obj.last_name, mobile_number=obj.mobile_number, dob=obj.dob, country=obj.country)
            job_seeker.save()


admin.site.register(CustomUser, CustomUserAdmin)


class CustomUserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.username


class JobProviderForm(forms.ModelForm):
    user = CustomUserModelChoiceField(
        queryset=CustomUser.objects.filter(user_type='Job Provider'))

    class Meta:
        model = JobProvider
        fields = '__all__'


class JobseekerAdmin(admin.ModelAdmin):  # Corrected class name
    readonly_fields = ('username',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    # Customize the list of displayed fields and any other desired configurations


class JobProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')

    form = JobProviderForm

    # Customize the list of displayed fields and any other desired configurations
admin.site.site_header = 'OPUS'
admin.site.register(Jobseeker, JobseekerAdmin)  # Corrected class name

admin.site.register(JobProvider, JobProviderAdmin)
