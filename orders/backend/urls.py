from django.urls import path, include
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm, \
    ResetPasswordRequestTokenViewSet, ResetPasswordConfirmViewSet
from rest_framework.routers import DefaultRouter

from backend.views import PartnerUpdate, RegisterAccount, LoginAccount, CategoryView, ShopView, ProductInfoView, \
    BasketView, \
    AccountDetails, ContactView, OrderView, PartnerState, PartnerOrders, ConfirmAccount

app_name = 'backend'

router = DefaultRouter()  # Простой роутер без маршрутов для деталей и списков

router.register(r'partner/update', PartnerUpdate, basename='partner-update')
router.register(r'partner/state', PartnerState, basename='partner-state')
router.register(r'partner/order', PartnerOrders, basename='partner-orders')
#
router.register(r'user/register', RegisterAccount, basename='user-register')
router.register(r'user/register/confirm', ConfirmAccount, basename='user-register-confirm')
router.register(r'user/details', AccountDetails, basename='user-details')
router.register(r'user/contact', ContactView, basename='user-contact')
router.register(r'user/login', LoginAccount, basename='user-login')
router.register(r'user/password_reset', ResetPasswordRequestTokenViewSet, basename='password-reset')
router.register(r'user/password_reset/confirm', ResetPasswordConfirmViewSet, basename='password-reset-confirm')
#
router.register(r'categories', CategoryView, basename='categories')
router.register(r'shops', ShopView, basename='shops')
router.register(r'products', ProductInfoView, basename='products')
router.register(r'basket', BasketView, basename='basket')
router.register(r'order', OrderView, basename='order')

# router.get_routes()

urlpatterns = [
    path('', include(router.urls)),

    # path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    # path('partner/state', PartnerState.as_view(), name='partner-state'),
    # path('partner/order', PartnerOrders.as_view(), name='partner-orders'),
    # path('partner/order/<int:pk>/', PartnerOrders.as_view(), name='partner-orders-detail'),

    # path('user/register', RegisterAccount.as_view(), name='user-register'),
    # path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    # path('user/details', AccountDetails.as_view(), name='user-details'),
    # path('user/contact', ContactView.as_view(), name='user-contact'),
    # path('user/login', LoginAccount.as_view(), name='user-login'),
    # path('user/password_reset', reset_password_request_token, name='password-reset'),
    # path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    # path('categories', CategoryView.as_view(), name='categories'),
    # path('shops', ShopView.as_view(), name='shops'),
    # path('products', ProductInfoView.as_view(), name='products'),
    # path('products/<int:pk>/', ProductInfoView.as_view(), name='product-detail'),

    # path('basket', BasketView.as_view(), name='basket'),
    # path('order', OrderView.as_view(), name='order'),
    # path('order/<int:pk>/', OrderView.as_view(), name='order-detail'),
]
