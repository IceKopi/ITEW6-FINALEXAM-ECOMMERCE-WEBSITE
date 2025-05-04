from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderListCreateView, OrderItemCreateView, CheckoutLogListView, RegisterView, CheckoutLogCreateView, AdminOrderListView, OrderItemCreateView, CompleteOrderView
from .views import user_info
from django.conf import settings
from django.conf.urls.static import static
from . import views



router = DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderListCreateView.as_view()),
    path('order-items/', OrderItemCreateView.as_view()),
    path('checkout-logs/create/', CheckoutLogCreateView.as_view()),
    path('admin-orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('cart/complete/', views.CompleteOrderView.as_view(), name='complete-order'),
    path('orders/complete/', CompleteOrderView.as_view(), name='complete-order'),
    path('cart/current/', views.CurrentCartView.as_view(), name='current-cart'),
    path('checkout-logs/', CheckoutLogListView.as_view()),
    path('register/', RegisterView.as_view()),
    path('user/', user_info),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)