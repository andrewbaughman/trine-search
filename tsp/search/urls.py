from django.urls import path, include
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from search import views

urlpatterns = [
	path('', views.index, name='index'),
	path('search/admin/', admin.site.urls),
	path('results/<query>/', views.results, name='results'),
	path('api/', views.PageList.as_view()),
	path('api/<int:pk>/', views.PageDetail.as_view()),
	path('api-auth/', include('rest_framework.urls')),
	path('add_page/', views.AddPage.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)