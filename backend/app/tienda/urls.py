"""
URL mapping for the user API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tienda import views


app_name = 'tienda'

router = DefaultRouter()
router.register(r'articulo', views.ArticulosViewSet)
router.register(r'sine', views.SineSeriesViewSet)
router.register(r'cosine', views.CosineSeriesViewSet)
router.register(r'tangent', views.TangentSeriesViewSet)

urlpatterns = [
    path('', include(router.urls), name = 'list'),
    path('run-sql-query/', views.RunSQLQueryView.as_view(), name='run-sql-query'),
]