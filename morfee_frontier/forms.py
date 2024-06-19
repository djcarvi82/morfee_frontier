from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label = 'Usuario',
        widget = forms.TextInput(attrs={'autocapitalize': 'off', 'autofocus': True, 'class': 'form-control', 'placeholder': 'Usuario', 'autocomplete': 'off'})
    )
    password = forms.CharField(
        label = 'Contraseña',
        strip = False,
        widget = forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control mb-10'})
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label = 'Contraseña actual',
        widget = forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Digite aquí su contraseña actual'})
    )
    new_password1 = forms.CharField(
        label = 'Nueva contraseña',
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite aquí su nueva contraseña'})
    )
    new_password2 = forms.CharField(
        label = 'Nueva contraseña (repetición por seguridad)',
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite aquí nuevamente su nueva contraseña'})
    )
