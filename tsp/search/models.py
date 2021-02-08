from django.db import models

# Create your models here.

class page(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.URLField(max_length=200)
	title = models.CharField(max_length=50)
	description = models.TextField(max_length=400)


class keywords(models.Model):
	url = models.ForeignKey('links', on_delete=models.CASCADE)
	keyword = models.CharField(max_length=50)
	times_on_page = models.IntegerField()


class links(models.Model):
	destination = models.URLField(max_length=200, primary_key=True)
	source = models.URLField(max_length=200)
	isTrine = models.BooleanField()
	visited = models.BooleanField()


class page_results(models.Model):
	url = models.ForeignKey('links', on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=250)