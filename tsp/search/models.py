from django.db import models

# Create your models here.

class page(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.URLField(max_length=200)
	title = models.CharField(max_length=50)
	description = models.TextField(max_length=400)