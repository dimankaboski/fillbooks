from main.models import ShippingBlank
from django import forms


class ShippingBlankEdit(forms.ModelForm):

    class Meta:
        model = ShippingBlank
        fields = (
            'top', 'bottom'
        )