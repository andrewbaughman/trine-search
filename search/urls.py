from django.urls import path, include
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from search import views

urlpatterns = [
	path('', views.index, name='index'),
	path('search/admin/', admin.site.urls),
	path('results/', views.results, name='results'),
	path('trine-results/', views.trine_results, name='trine_results'),
	path('images/', views.image_results, name='image_results'),
	path('api/', views.PageList.as_view()),
	path('api/<int:pk>/', views.PageDetail.as_view()),
	path('api/links/', views.LinksList.as_view()),
	path('api/links/<int:pk>/', views.LinksDetail.as_view()),
	path('api/image/', views.ImageList.as_view()),
	path('api/image/<int:pk>/', views.ImageDetail.as_view()),
	path('api/keywords/', views.KeywordsList.as_view()),
	path('api/keywords/<int:pk>/', views.KeywordsDetail.as_view()),
	path('api/edges/', views.EdgesList.as_view()),
	path('api/edges/<int:pk>/', views.EdgesDetail.as_view()),
	path('users/', views.UserList.as_view()),
	path('users/<int:pk>/', views.UserDetail.as_view()),
	path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)