from django import forms

CHOICES = ((1, 'Banking'), (2, 'Beverages'), (3, 'Entertainment'), (4, 'Retail Corporation'), (5, 'Telecomunication'))

class Industry(forms.Form):
    choice = forms.ChoiceField(
        widget=forms.RadioSelect, 
        choices=CHOICES,
        label='Choice of Industry'
        )