from django import forms
from .models import Supporter

class NewsletterForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        max_length=254,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "seu@email.com"}),
    )

class SupporterForm(forms.ModelForm):
    class Meta:
        model = Supporter
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}), # Ativa o calendário do navegador
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica estilo Tailwind em todos os campos automaticamente
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-[#E87A4F] focus:ring-2 focus:ring-[#E87A4F]/20 outline-none transition'
            field.widget.attrs['placeholder'] = field.label