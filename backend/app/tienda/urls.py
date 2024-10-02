"""
URL mapping for the user API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tienda import views


app_name = 'tienda'

router = DefaultRouter()
router.register(r'articulo', views.ArticulosViewSet)

urlpatterns = [
    path('', include(router.urls), name = 'list'),
    path('run-sql-query/', views.RunSQLQueryView.as_view(), name='run-sql-query'),
    path('sine/', views.SineSeriesViewSet.as_view(), name=)
]