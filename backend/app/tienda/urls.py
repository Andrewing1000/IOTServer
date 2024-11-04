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
router.register(r'user', views.CreateIOTClient)
router.register(r'fibonacci', views.FibonacciViewSet)

urlpatterns = [
    path('', include(router.urls), name = 'list'),
    path('run-sql-query/', views.RunSQLQueryView.as_view(), name='run-sql-query'),
    path('activity/', views.ActivityView.as_view(), name='activity'),
    path('iotinterface/', views.FibonacciInterface.as_view(), name='fibonacci_interface'),
    path('login/', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
    path('admin/', views.admin_view, name='admin')
]