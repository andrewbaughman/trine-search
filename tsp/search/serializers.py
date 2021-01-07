from rest_framework import serializers
from .models import page
from django.contrib.auth.models import User

class PageSerializer(serializers.ModelSerializer):

	class Meta:
		model = page
		fields = ('id', 'url', 'title', 'description',)

class UserSerializer(serializers.ModelSerializer):
	pages = serializers.PrimaryKeyRelatedField(
		many=True, queryset=page.objects.all())

	class Meta:
		model = User
		fields = ('id', 'username', 'pages')