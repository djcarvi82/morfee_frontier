from django import forms

class AgendaForm(forms.Form):
    g_r = forms.CharField(label='Reserva', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    g_o = forms.CharField(label='Operador', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    l_p = forms.CharField(label='Puesto de salud', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    t_f = forms.DateField(label='Fecha', required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'AAAA-MM-DD'}))
    t_h = forms.CharField(label='Hora', required=True, widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM'}))
