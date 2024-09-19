from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet

router = DefaultRouter()
router.register(r'api/v1/wallet', WalletViewSet, basename='wallet')

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/wallet/<str:pk>/operation/', WalletViewSet.as_view({'post': 'create_operation'}), name='wallet-create-operation'),
]