from django import forms

class NewsletterForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        max_length=254,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "seu@email.com"}),
    )