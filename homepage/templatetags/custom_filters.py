from django import template
from jobpost.models import Job
register = template.Library()


@register.filter
def split(value, delimiter):
    return value.split(delimiter)


@register.filter
def count_items(queryset):
    return len(queryset)


@register.filter
def filter_category(jobs, category_id):
    return Job.objects.filter(category_id=category_id)
