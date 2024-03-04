from django.urls import path
from . import views

urlpatterns = [
     path('providerdash/', views.providerdash, name='providerdash'),
     path('editjob/<int:job_id>/', views.editjob, name='editjob'),
     path('providerhome/', views.providerhome, name='providerhome'),
     path('alljobs/', views.alljobs, name='alljobs'),
     path('createjob/', views.createjob, name='createjob'),
     path('applications/', views.applications, name='applications'),
     path('acceptedjob/<int:application_id>/',
          views.acceptedjobwithid, name='acceptedjob'),
     path('acceptedjob', views.acceptedjob, name='acceptedjob'),
     path('rejectedjob', views.rejectedjob, name='rejectedjob'),
     path('rejectedjob/<int:application_id>/',
          views.rejectedjobwithid, name='rejectedjob'),
     path('deleteapplicationwithid/<int:application_id>/',
          views.deleteapplicationwithid, name='deleteapplicationwithid'),
     path('send_offer/<int:application_id>/',
          views.send_offer, name='send_offer'),
          
     path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
     path('apply_view/<int:job_id>/', views.apply_view, name='apply_view'),
     path('show_notification/', views.show_notification, name='show_notification'),
     path('notifications/mark-as-read/<int:notification_id>/',
          views.mark_notification_as_read, name='mark_notification_as_read'),
     path('notifications/delete_notification/<int:notification_id>/',
          views.delete_notification, name='delete_notification'),

]
