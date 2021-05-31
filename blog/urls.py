from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('file_upload/', views.upload, name='upload'),
    path('contact/', views.contact_us, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),
    # path('', views.index, name='index')
]