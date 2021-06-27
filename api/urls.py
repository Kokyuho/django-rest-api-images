from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('job-list/', views.jobList, name="job-list"),
	path('job-detail/<str:pk>/', views.JobDetail, name="job-detail"),
	path('job-create/', views.JobCreate, name="job-create"),
	path('job-update/<str:pk>/', views.JobUpdate, name="job-update"),
	path('job-delete/<str:pk>/', views.JobDelete, name="job-delete"),
	path('job-run/<str:pk>/', views.JobRun, name="job-run"),
]
