from enum import unique
from django import forms
from django.db.models.query import QuerySet
from users.models import AuthCliente, AuthModulo, AuthRol, UserMorfee

CHOICES = [('sp', 'Salud Pública'), ('ase', 'Aseguramiento')]

class ClienteForm(forms.Form):
    cliente = forms.CharField(max_length=100, required=True, label='Nombre del cliente / empresa:', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'El nombre del cliente y/o empresa es requerido!'})
    direccion = forms.CharField(max_length=100, required=True, label='Dirección del cliente / empresa:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'La dirección del cliente y/o empresa es requerido!'})
    correo = forms.CharField(max_length=100, required=True, label='Correo electrónico:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'El correo electrónico es requerido!'})
    contacto = forms.CharField(max_length=100, required=True, label='Nombre del contacto:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'El nombre del contacto es requerido!'})
    modulos = forms.MultipleChoiceField(
        required=False, 
        label='Seleccione los módulos a habilitar:', 
        widget=forms.CheckboxSelectMultiple, 
        choices=AuthModulo.objects.values_list('clave', 'modulo')
    )
    is_indigena = forms.BooleanField(required=False, label='La EPS es indígena:')

class ModuloForm(forms.ModelForm):
    modulo = forms.CharField(max_length=30, required=True, label='Nombre del módulo:', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'El nombre del módulo es requerido!'})
    descripcion = forms.CharField(max_length=250, required=True, label='Descripción del módulo:', widget=forms.Textarea(attrs={'class': 'form-control'}), error_messages={'required': 'La descripción es requerida!'})
    clave = forms.CharField(max_length=10, required=True, label='Clave del módulo:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'La clave módulo es requerida!'})
    estado = forms.ChoiceField(required=True, label='Estado del módulo:', widget=forms.RadioSelect, choices=[('build', 'En construcción'), ('active', 'Activo')], error_messages={'required': 'Debe indicar el estado del módulo!'})

    class Meta:
        model = AuthModulo
        fields = ['modulo', 'descripcion', 'clave', 'estado']

class RolForm(forms.ModelForm):
    rol = forms.CharField(max_length=20, required=True, label='Nombre del rol de usuario:', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'El nombre del rol de usuario es requerido!'})
    nivel = forms.IntegerField(required=True, label='Nivel:', widget=forms.NumberInput(attrs={'class': 'form-control'}), error_messages={'required': 'El nivel es requerida!'})

    class Meta:
        model = AuthRol
        fields = ['rol', 'nivel']

class UserMorfeeForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, label="Usuario:", widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}), error_messages={'unique': 'El nombre de usuario ingresado no está disponible!'})
    password1 = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), error_messages={'required': 'La contraseña es requerida!'})
    password2 = forms.CharField(label="Confirmación", widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), strip=False, error_messages={'required': 'La confirmación de contraseña es obligatoria!'})
    first_name = forms.CharField(max_length=100, required=True, label='Nombres:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los nombres del usuario son requeridos!'})
    last_name = forms.CharField(max_length=100, required=True, label='Apellidos:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los apellidos del usuario son requeridos!'})
    email = forms.EmailField(label="Correo electrónico", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'off', 'class': 'form-control'}))
    cliente = forms.ModelChoiceField(label="Cliente y/o empresa:", queryset=AuthCliente.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione el cliente")
    rol = forms.ModelChoiceField(label="Rol del usuario:", queryset=AuthRol.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione el rol")

    class Meta:
        model = UserMorfee
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'cliente', 'rol']

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Las contraseñas no coinciden!")
        return pw2

class UserClientForm(forms.ModelForm):
    
    def __init__(self, daky, *args, **kwargs):
        super(UserClientForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = AuthCliente.objects.filter(pk=daky)

    username = forms.CharField(max_length=100, required=True, label="Usuario:", widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}), error_messages={'unique': 'El nombre de usuario ingresado no está disponible!'})
    password1 = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), error_messages={'required': 'La contraseña es requerida!'})
    password2 = forms.CharField(label="Confirmación", widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), strip=False, error_messages={'required': 'La confirmación de contraseña es obligatoria!'})
    first_name = forms.CharField(max_length=100, required=True, label='Nombres:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los nombres del usuario son requeridos!'})
    last_name = forms.CharField(max_length=100, required=True, label='Apellidos:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los apellidos del usuario son requeridos!'})
    email = forms.EmailField(label="Correo electrónico", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'off', 'class': 'form-control'}))
    cliente = forms.ModelChoiceField(label="Cliente y/o empresa:", queryset=None, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione el cliente")
    rol = forms.ModelChoiceField(label="Rol del usuario:", queryset=AuthRol.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione el rol")

    class Meta:
        model = UserMorfee
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'cliente', 'rol']

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Las contraseñas no coinciden!")
        return pw2

class UserStaffForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, label="Usuario:", widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}), error_messages={'unique': 'El nombre de usuario ingresado no está disponible!'})
    password1 = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), error_messages={'required': 'La contraseña es requerida!'})
    password2 = forms.CharField(label="Confirmación", widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), strip=False, error_messages={'required': 'La confirmación de contraseña es obligatoria!'})
    first_name = forms.CharField(max_length=100, required=True, label='Nombres:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los nombres del usuario son requeridos!'})
    last_name = forms.CharField(max_length=100, required=True, label='Apellidos:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los apellidos del usuario son requeridos!'})
    email = forms.EmailField(label="Correo electrónico", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'off', 'class': 'form-control'}))

    class Meta:
        model = UserMorfee
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'cliente']

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Las contraseñas no coinciden!")
        return pw2

class UserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, label="Usuario:", widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}), error_messages={'unique': 'El nombre de usuario ingresado no está disponible!'})
    first_name = forms.CharField(max_length=100, required=True, label='Nombres:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los nombres del usuario son requeridos!'})
    last_name = forms.CharField(max_length=100, required=True, label='Apellidos:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los apellidos del usuario son requeridos!'})
    email = forms.EmailField(label="Correo electrónico", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'off', 'class': 'form-control'}))
    cliente = forms.ModelChoiceField(label="Cliente y/o empresa:", queryset=AuthCliente.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione el cliente")
    rol = forms.ModelChoiceField(label="Rol del usuario:", queryset=AuthRol.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione el rol")

    class Meta:
        model = UserMorfee
        fields = ['username', 'first_name', 'last_name', 'email', 'cliente', 'rol']

class UserEditStaffForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, label="Usuario:", widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}), error_messages={'unique': 'El nombre de usuario ingresado no está disponible!'})
    first_name = forms.CharField(max_length=100, required=True, label='Nombres:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los nombres del usuario son requeridos!'})
    last_name = forms.CharField(max_length=100, required=True, label='Apellidos:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los apellidos del usuario son requeridos!'})
    email = forms.EmailField(label="Correo electrónico", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'off', 'class': 'form-control'}))

    class Meta:
        model = UserMorfee
        fields = ['username', 'first_name', 'last_name', 'email', 'cliente']

class UserClientEditForm(forms.ModelForm):

    def __init__(self, daky, *args, **kwargs):
        super(UserClientEditForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = AuthCliente.objects.filter(pk=daky)

    username = forms.CharField(max_length=100, required=True, label="Usuario:", widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}), error_messages={'unique': 'El nombre de usuario ingresado no está disponible!'})
    first_name = forms.CharField(max_length=100, required=True, label='Nombres:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los nombres del usuario son requeridos!'})
    last_name = forms.CharField(max_length=100, required=True, label='Apellidos:', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), error_messages={'required': 'Los apellidos del usuario son requeridos!'})
    email = forms.EmailField(label="Correo electrónico", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'off', 'class': 'form-control'}))
    cliente = forms.ModelChoiceField(label="Cliente y/o empresa:", queryset=None, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione el cliente")
    rol = forms.ModelChoiceField(label="Rol del usuario:", queryset=AuthRol.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione el rol")

    class Meta:
        model = UserMorfee
        fields = ['username', 'first_name', 'last_name', 'email', 'cliente', 'rol']
