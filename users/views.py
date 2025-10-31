from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from reportlab.pdfgen import canvas
from io import BytesIO

from .models import (
    Profile,
    Reservation,
    Folio,
    Invoice,
    CreditNote,
    DebitNote
)
from .serializers import (
    ProfileSerializer,
    RegisterSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ReservationSerializer,
    FolioSerializer,
    InvoiceSerializer,
    CreditNoteSerializer,
    DebitNoteSerializer
)

# ---------------------------
# Profile Views
# ---------------------------

class ProfileCreateAPIView(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'


class ProfileDetailAPIView(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Profile, pk=pk)
        obj.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ProfileListCreateAPIView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# ---------------------------
# Authentication Views
# ---------------------------

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Password updated successfully!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Implement sending email logic here
            return Response({"detail": "Password reset link sent to email."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Implement password reset logic here
            return Response({"detail": "Password has been reset."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# Reservation Views
# ---------------------------

class ReservationListAPIView(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class ReservationCreateAPIView(CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class ReservationDetailAPIView(RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class ReservationUpdateAPIView(UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class ReservationDeleteAPIView(DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


# ---------------------------
# Folio Views
# ---------------------------

class FolioListAPIView(ListAPIView):
    queryset = Folio.objects.all()
    serializer_class = FolioSerializer
    permission_classes = [IsAuthenticated]


class FolioDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        folio = get_object_or_404(Folio, pk=pk)
        serializer = FolioSerializer(folio)
        return Response(serializer.data)

    def put(self, request, pk):
        folio = get_object_or_404(Folio, pk=pk)
        serializer = FolioSerializer(folio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        folio = get_object_or_404(Folio, pk=pk)
        folio.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class FolioViewSet(viewsets.ModelViewSet):
    queryset = Folio.objects.all()
    serializer_class = FolioSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsAuthenticated]


class FolioCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FolioSerializer(data=request.data)
        if serializer.is_valid():
            folio = serializer.save()
            return Response(FolioSerializer(folio).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# Invoice, CreditNote, and DebitNote Views
# ---------------------------

class InvoiceCreateAPIView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceDetailAPIView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'id'


class InvoicePDFAPIView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        invoice = self.get_object()

        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Invoice #{invoice.id}")
        p.drawString(100, 780, f"Customer: {invoice.customer.name}")
        p.drawString(100, 760, f"Amount: ${invoice.total_amount}")
        p.drawString(100, 740, f"Due Date: {invoice.due_date}")
        p.showPage()
        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')


class CreditNoteAPIView(generics.CreateAPIView):
    serializer_class = CreditNoteSerializer

    def create(self, request, *args, **kwargs):
        invoice_id = kwargs.get('id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(invoice_id=invoice_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DebitNoteAPIView(generics.CreateAPIView):
    serializer_class = DebitNoteSerializer

    def create(self, request, *args, **kwargs):
        invoice_id = kwargs.get('id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(invoice_id=invoice_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
