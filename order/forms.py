from django import forms
from .models import Order, Payment
import re

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01XXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2 (Optional)'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Division'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'order_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special instructions...'}),
        }
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^01[3-9]\d{8}$', phone):
            raise forms.ValidationError("Please enter a valid Bangladeshi phone number (e.g., 01712345678)")
        return phone

class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
        ('upay', 'Upay'),
        ('card', 'Credit/Debit Card'),
        ('emi', 'EMI'),
        ('cod', 'Cash On Delivery'),
    ]

    EMI_CHOICES = [
        (3, '3 Months'),
        (6, '6 Months'),
        (12, '12 Months'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'payment-method-radio'}),
        label="Select Payment Method",
        required=True
    )

    # Mobile payment fields
    mobile_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mobile-field',
            'placeholder': '01XXXXXXXXX',
            'pattern': '01[3-9][0-9]{8}'
        }),
        label="Mobile Number"
    )

    transaction_id = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mobile-field',
            'placeholder': 'Transaction ID'
        }),
        label="Transaction ID"
    )

     # Card payment fields
    card_number = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control card-field',
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9\s]{13,19}'
        }),
        label="Card Number"
    )

    card_holder_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control card-field',
            'placeholder': 'Card Holder Name'
        }),
        label="Card Holder Name"
    )

    expiry_date = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control card-field',
            'placeholder': 'MM/YY',
            'pattern': '(0[1-9]|1[0-2])\/[0-9]{2}'
        }),
        label="Expiry Date"
    )

    cvv = forms.CharField(
        max_length=3,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control card-field',
            'placeholder': 'CVV',
            'pattern': '[0-9]{3}'
        }),
        label="CVV"
    )

     # EMI field
    emi_month = forms.ChoiceField(
        choices=EMI_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'emi-radio'}),
        label="EMI Duration"
    )

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        #moile payment validation:
        if payment_method in ['bkash', 'nagad', 'rocket', 'upay']:
            mobile_number = cleaned_data.get('mobile_number')
            transaction_id = cleaned_data.get('transaction_id')
            
            if not mobile_number:
                self.add_error('mobile_number', f"Mobile number is required for {payment_method} payment")


            if not transaction_id:
                self.add_error('transaction_id', f"Transaction ID is required for {payment_method} payment")

            if mobile_number and not re.match(r'^01[3-9]\d{8}$', mobile_number):
                self.add_error('mobile_number', "Please enter a valid Bangladeshi mobile number")
        
        # Card payment validation
        elif payment_method == 'card':
            card_number = cleaned_data.get('card_number')
            card_holder_name = cleaned_data.get('card_holder_name')
            expiry_date = cleaned_data.get('expiry_date')
            cvv = cleaned_data.get('cvv')

            if not card_number:
                self.add_error('card_number', "Card number is required for card payment")
            
            elif not self.luhn_check(card_number.replace(" ", "")):
                self.add_error('card_number', "Please enter a valid card number")

            if not card_holder_name:
                self.add_error('card_holder_name', "Card holder name is required for card payment")

            if not expiry_date:
                self.add_error('expiry_date', "Expiry date is required")
            elif not re.match(r'^(0[1-9]|1[0-2])\/[0-9]{2}$', expiry_date):
                self.add_error('expiry_date', "Please enter expiry date in MM/YY format")
            
            if not cvv:
                self.add_error('cvv', "CVV is required for card payment")
            elif not re.match(r'^[0-9]{3}$', cvv):
                self.add_error('cvv', "CVV must be 3 digits")



        # EMI validation
        elif payment_method == 'emi':
            emi_month = cleaned_data.get('emi_month')
            card_number = cleaned_data.get('card_number')

            if not emi_month:
                self.add_error('emi_month', "Please select EMI duration.")

            if not card_number:
                self.add_error('card_number', "Card number is required for EMI.")

            elif card_number and not self.luhn_check(card_number.replace(" ", "")):
                self.add_error('card_number', "Please enter a valid card number")

        return cleaned_data
    
    def luhn_check(self, card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10 == 0
            
            
            

            # #card payment validation:
            # elif payment_method == 'card':
            #     if not cleaned_data.get('card_number'):
            #         raise forms.ValidationError("Card Number is required for card payment")
            #     if not cleaned_data.get('card_holder_name'):
            #         raise forms.ValidationError("Card Holder Name is required for card payment")
            #     if not cleaned_data.get('expiry_date'):
            #         raise forms.ValidationError("Expiry Date is required for card payment")
            #     if not cleaned_data.get('cvv'):
            #         raise forms.ValidationError("CVV is required for card payment")
                
            # # EMI validation:
            # elif payment_method == 'emi':
            #     if not cleaned_data.get('emi_month'):
            #         raise forms.ValidationError("Please select EMI duration.")
            #     if not cleaned_data.get('card_number'):
            #         raise forms.ValidationError("Card number is required for EMI.")
        
            # return cleaned_data
