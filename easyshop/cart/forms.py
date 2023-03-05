from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """
    A form to add products to the cart with quantity and update options
    """
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
        label="Update quantity"
    )
