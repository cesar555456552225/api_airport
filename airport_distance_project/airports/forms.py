from django import forms

class AirportDistanceForm(forms.Form):
    aeropuerto_origen = forms.charfield(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Ej: CCS',
            'pattern':'[A-Z]{3}',
            'title':'Ingrese código IATA del aeropuerto'
        }),
        label='Aeropuerto origen (Código IATA)'
    )

    aeropuerto_destino = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Ej: TOK',
            'pattern':'[A-Z]{3}',
            'title':'Ingrese el código IATA del aeropuerto destino'
        }),
        label='Aeropuerto destino (Código IATA)'
    )
    
    def clean_aeropuerto_origen(self):
        codigo = self.cleaned_data['aeropuerto_origen'].upper()
        if not codigo.isalpha():
            raise forms.ValidationError("El código IATA debe contener solo letras.")
        return codigo
    
    def clean_aeropuerto_destino(self):
        codigo = self.cleaned_data['aeropuerto_destino'].upper()
        if not codigo.isalpha():
            raise forms.ValidationError("El código IATA debe contener solo letras.")
        return codigo