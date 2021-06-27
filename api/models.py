from django.db import models

# Create your models here.

class Job(models.Model):
  res_list = models.CharField(max_length=200)
  r_list = models.CharField(max_length=200)
  g_list = models.CharField(max_length=200)
  b_list = models.CharField(max_length=200)
  status = models.CharField(max_length=50, default='Pending')
  output = models.CharField(max_length=300, default='', blank=True)
