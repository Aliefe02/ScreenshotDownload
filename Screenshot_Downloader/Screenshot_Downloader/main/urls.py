from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('download/<str:Filename>',views.download,name='download'),
    path('CreateZip',views.CreateZip,name='CreateZip'),
]