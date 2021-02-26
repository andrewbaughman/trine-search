from django.db import models

# Create your models here.

class page(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.ForeignKey('links', on_delete=models.CASCADE, to_field="destination", db_column="url")
	title = models.CharField(max_length=50)
	description = models.TextField(max_length=400)


class keywords(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.ForeignKey('links', on_delete=models.CASCADE)
	keyword = models.CharField(max_length=50)
	times_on_page = models.IntegerField()


class links(models.Model):
	id = models.AutoField(primary_key=True)
	pagerank = models.DecimalField(max_digits=5, decimal_places=4, null=True)
	destination = models.URLField(max_length=200, unique=True)
	source = models.URLField(max_length=200)
	isTrine = models.BooleanField()
	visited = models.BooleanField()


class edges(models.Model):
	id = models.AutoField(primary_key=True)
	pointA = models.ForeignKey('links', related_name="pointA", on_delete=models.CASCADE)
	pointB = models.ForeignKey('links', related_name="pointB", on_delete=models.CASCADE)


class page_results(models.Model):
	url = models.ForeignKey('links', on_delete=models.CASCADE, to_field="destination", db_column="url")
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=250)