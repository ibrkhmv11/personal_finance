from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    RegisterView, LogoutView,
    WalletListCreateAPIView, WalletDetailAPIView,
    CategoryListCreateAPIView, CategoryDetailAPIView,
    TransactionListCreateAPIView, TransactionDetailAPIView,
    StatisticsAPIView
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', obtain_auth_token, name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    path('wallets/', WalletListCreateAPIView.as_view(), name='wallet-list-create'),
    path('wallets/<int:pk>/', WalletDetailAPIView.as_view(), name='wallet-detail'),

    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    path('transactions/', TransactionListCreateAPIView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionDetailAPIView.as_view(), name='transaction-detail'),

    path('statistics/', StatisticsAPIView.as_view(), name='statistics'),
]