from django import forms


class OrderForm(forms.Form):
    phone_number = forms.CharField(required=False)
    email = forms.EmailField(required=False)
