from django.contrib import admin
from .models import Categories, Blog, Comment, Feedback
# Register your models here.

admin.site.register(Categories)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Feedback)
