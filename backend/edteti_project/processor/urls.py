from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/<int:pk>/', views.file_detail, name='file_detail'),
    path('apply-filter/<int:pk>/<str:filter_type>/', views.apply_filter, name='apply_filter'),
    path('extract-roi/<int:pk>/', views.extract_roi, name='extract_roi'),
    path('video-segment/<int:pk>/', views.create_video_segment, name='create_video_segment'),
]
