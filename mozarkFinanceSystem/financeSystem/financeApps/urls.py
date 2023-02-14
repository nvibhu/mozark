from django.urls import include, path
from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
# ]

urlpatterns = [
    path('files/', views.files, name='files'),
    path('files/details/<str:file_name>', views.details, name='details'),
]