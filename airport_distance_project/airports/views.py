from django.shortcuts import render
from django.http import JsonResponse
from django .shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import requests
# Create your views here.


def airport_distance_view(request):
    return render(request, 'airport_distance.html')

@csrf_exempt

def calculate_distance(request):
    if request.method=='POST':
        try:
            aeropuerto_origen = request.POST.get('aeropuerto_origen', '').strip().upper()
            aeropuerto_destino = request.POST.get('aeropuerto_destino', '').strip().upper()

            if not aeropuerto_destino or not aeropuerto_destino:
                return JsonResponse({
                    'succes': False,
                    'error': 'Debe ingresar los dos codigos IATA de cada aeropuerto.'
                })
            if len(aeropuerto_origen) !=3 or len(aeropuerto_destino) !=3:
                return JsonResponse({
                    'succes':False,
                    'error': 'Los codigo IATA solo deben contener 3 caracteres.'
                })
            
            if aeropuerto_origen == aeropuerto_destino:
                return JsonResponse({
                    'succes': False,
                    'error': 'El origen y destino no pueden ser iguales.'
                })
            base_url = "https://airportgap.com/api/airports/distance"

            airport_data ={
                "from":aeropuerto_origen,
                "to":aeropuerto_destino
            }

            response_post = request.post(base_url, json=airport_data, Timeout = 10)

            if response_post.status_code == 200:
                datos = response_post.json()

                result_data = {
                    'succes': True,
                    'codigo': datos["data"]["id"],
                    'aeropuerto_origen':{
                        'nombre':datos["data"]["atributes"]["from_airport"]["name"],
                        'ciudad':datos["data"]["atributes"]["from_airport"]["city"],
                        'codigo':aeropuerto_origen
                    }
                }