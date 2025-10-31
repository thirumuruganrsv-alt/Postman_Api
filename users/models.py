from django.db import models
from django.conf import settings
from django.utils import timezone

# ---------------------------
# Profile Model
# ---------------------------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# ---------------------------
# Reservation Model
# ---------------------------
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.CharField(max_length=100)
    checkin = models.DateTimeField()
    checkout = models.DateTimeField(default=timezone.now)  # Default prevents migration prompt
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Reservation of {self.room} by {self.user.username} from {self.checkin} to {self.checkout}"


# ---------------------------
# Folio Model
# ---------------------------
class Folio(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Folio for {self.reservation.user.username} - Total: {self.total_amount}"


# ---------------------------
# Customer Model
# ---------------------------
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


# ---------------------------
# Invoice Model
# ---------------------------
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.customer.name}"


# ---------------------------
# Credit Note Model
# ---------------------------
class CreditNote(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='credit_notes')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Credit Note for Invoice #{self.invoice.id} - Amount: {self.amount}"


# ---------------------------
# Debit Note Model
# ---------------------------
class DebitNote(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='debit_notes')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Debit Note for Invoice #{self.invoice.id} - Amount: {self.amount}"
