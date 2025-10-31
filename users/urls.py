from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    RegisterView,
    LogoutView,
    ChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
    ProfileListCreateAPIView,
    ProfileDetailAPIView,
    ReservationListAPIView,
    ReservationViewSet,
    FolioCreateAPIView,
    FolioDetailAPIView,
    InvoiceCreateAPIView,
    InvoiceDetailAPIView,
    InvoicePDFAPIView,
    CreditNoteAPIView,
    DebitNoteAPIView,
)

# ---------------------------
# Router for Reservation ViewSet
# ---------------------------
router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    # ============================
    # AUTHENTICATION
    # ============================
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # JWT Token Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # ============================
    # PASSWORD MANAGEMENT
    # ============================
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    # ============================
    # PROFILE MANAGEMENT
    # ============================
    path('profiles/', ProfileListCreateAPIView.as_view(), name='profile_list_create'),
    path('profiles/<int:pk>/', ProfileDetailAPIView.as_view(), name='profile_detail'),

    # ============================
    # FOLIO MANAGEMENT
    # ============================
    path('folios/', FolioCreateAPIView.as_view(), name='folio_create'),
    path('folios/<int:pk>/', FolioDetailAPIView.as_view(), name='folio_detail'),

    # ============================
    # RESERVATION MANAGEMENT
    # ============================
    path('reservations-list/', ReservationListAPIView.as_view(), name='reservation_list'),

    # ============================
    # BILLING & INVOICE
    # ============================
    path('invoices/', InvoiceCreateAPIView.as_view(), name='invoice_create'),
    path('invoices/<int:id>/', InvoiceDetailAPIView.as_view(), name='invoice_detail'),
    path('invoices/<int:id>/pdf/', InvoicePDFAPIView.as_view(), name='invoice_pdf'),
    path('invoices/<int:id>/credit-note/', CreditNoteAPIView.as_view(), name='credit_note_create'),
    path('invoices/<int:id>/debit-note/', DebitNoteAPIView.as_view(), name='debit_note_create'),

    # ============================
    # ROUTER (ViewSets)
    # ============================
    path('', include(router.urls)),
]
