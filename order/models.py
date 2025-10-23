from django.db import models
from accounts.models import Account
from store.models import Product, Variation
from carts.models import Coupon, DeliveryMethod
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
# Create your models here.


# for payment system:
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
        ('upay', 'Upay'),
        ('card', 'Credit/Debit Card'),
        ('emi', 'EMI'),
        ('cod', 'Cash On Delivery'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # For mobile payments
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    

    # For card payments
    card_number = models.CharField(max_length=20, blank=True, null=True)
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)

    expiry_date = models.CharField(max_length=10, blank=True, null=True)
    cvv = models.CharField(max_length=5, blank=True, null=True)

     # For EMI
    emi_month = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

     # Additional fields
    payment_details = models.JSONField(blank=True, null=True)  # For storing additional payment info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.payment_id} - {self.get_payment_method_display()}"

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = self.generate_payment_id()
        super().save(*args, **kwargs)

    def generate_payment_id(self):
        import random
        import string
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f'PAY{timestamp}{random_str}'

    def calculate_emi_amount(self, principal_amount):
        """Calculate EMI amount with interest"""
        if self.emi_month and self.emi_interest > 0:
            monthly_interest = self.emi_interest / 12 / 100
            emi_amount = (principal_amount * monthly_interest * (1 + monthly_interest)**self.emi_month) / ((1 + monthly_interest)**self.emi_month - 1)
            return round(emi_amount, 2)
        return principal_amount


class Order(models.Model):
    NEW = 'New'
    ACCEPTED = 'Accepted'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    REFUNDED = 'Refunded'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (ACCEPTED, 'Accepted'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
        (REFUNDED, 'Refunded'),
    ]

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, default='Bangladesh')
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    
    order_total = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Status fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.SET_NULL, null=True, blank=True)    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}' if self.address_line_2 else self.address_line_1

    def calculate_totals(self):
        from django.db.models import Sum
        order_products_total = OrderProduct.objects.filter(order=self).aggregate(
             total=Sum(models.F('product_price') * models.F('quantity'))
        )['total'] or 0
        self.order_total = order_products_total
        self.tax = (self.order_total * Decimal('0.01'))  # 1% VAT
        self.grand_total = self.order_total + self.tax + self.delivery_charge - self.discount
        self.save()



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

    @property
    def sub_total(self):
        return self.product_price * self.quantity
    
    class Meta:
        unique_together = ('order', 'product')
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'

#ai product ta ami error asle delete kore dio and oupo r 2 ta line ami comment kora teke uncomment kore rakho
