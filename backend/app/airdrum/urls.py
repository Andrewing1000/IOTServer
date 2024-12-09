from django.urls import path, include

from rest_framework.routers import DefaultRouter
from . import views

app_name = "airdrum"

router = DefaultRouter()
router.register(r'testing',views.TestingViewSet, basename='testing')
router.register(r'sound', views.InstrumentViewSet, basename='sound')
router.register(r'track', views.TrackViewSet, basename='track')
urlpatterns = [
    path('', views.index),
    path('interface/', views.drum_interface),
    path('', include(router.urls), )
]