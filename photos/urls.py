from django.urls import path

from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    path('rotateLeft/<str:pk>/', views.rotateLeft, name='rotateLeft'),
    #path('rotateRight/<str:pk>/', views.rotateRight, name='rotateRight'),
]
