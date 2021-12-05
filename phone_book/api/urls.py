from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, CompanyViewSet, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('employees', EmployeeViewSet)
router_v1.register('companies', CompanyViewSet)
router_v1.register('users', UserViewSet)

api_patterns_v1 = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls))
]

urlpatterns = [
    path('', include(api_patterns_v1))
]
