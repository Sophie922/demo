from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Application, Review
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'fio', 'phone')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[A-Za-z0-9]{6,}$', username):
            raise forms.ValidationError("Логин: только латиница и цифры, мин. 6 символов.")
        return username

    def clean_password1(self):
        pwd = self.cleaned_data.get('password1')
        if pwd and len(pwd) < 8:
            raise forms.ValidationError("Пароль должен быть не менее 8 символов.")
        return pwd

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['course', 'start_date', 'payment_method']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ДД.ММ.ГГГГ', 'id': 'date-input'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('card', 'Банковская карта'),
                ('sbp', 'СБП'),
                ('cash', 'Наличные')
            ])
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})}