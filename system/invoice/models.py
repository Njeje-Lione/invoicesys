from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}. Email: {self.email}'

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('mpesa', 'M-Pesa'), ('airtel_money', 'Airtel Money'), ('cash', 'Cash'), ('bank', 'Bank Payment')])
    paid_at = models.DateTimeField(auto_now_add=True)