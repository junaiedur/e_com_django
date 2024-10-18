from django import forms
from django.core.exceptions import ValidationError
from .models import Coupon  # Assuming you have a Coupon model


class ApplyCouponForm(forms.Form):
    code = forms.CharField(max_length=50, label="Coupon Code")

    def clean_code(self):
        code = self.cleaned_data['code']
        
        # Check if the coupon exists
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            raise ValidationError("This coupon is invalid.")

        # Check if the coupon is active or valid
        if not coupon.is_valid():
            raise ValidationError("This coupon code is expired or not applicable.")
        
        return code

