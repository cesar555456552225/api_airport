from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import requests
import json
# Create your views here.


def airport_distance_view(request):
    return render(request, 'airport_distance.html')

@csrf_exempt

def calculate_distance(request):
    if request.method=='POST':
        try:
            aeropuerto_origen = request.POST.get('aeropuerto_origen', '').strip().upper()
            aeropuerto_destino = request.POST.get('aeropuerto_destino', '').strip().upper()

            if not aeropuerto_origen or not aeropuerto_destino:
                return JsonResponse({
                    'success': False,
                    'error': 'Debe ingresar los dos codigos IATA de cada aeropuerto.'
                })
            if len(aeropuerto_origen) !=3 or len(aeropuerto_destino) !=3:
                return JsonResponse({
                    'success':False,
                    'error': 'Los codigo IATA solo deben contener 3 caracteres.'
                })
            
            if aeropuerto_origen == aeropuerto_destino:
                return JsonResponse({
                    'success': False,
                    'error': 'El origen y destino no pueden ser iguales.'
                })
            base_url = "https://airportgap.com/api/airports"

            airport_data ={
                "from":aeropuerto_origen,
                "to":aeropuerto_destino
            }

            response_post = requests.post(f"{base_url}/distance", json=airport_data, timeout = 10)

            if response_post.status_code == 200:
                datos = response_post.json()

                result_data = {
                    'success': True,
                    'codigo': datos["data"]["id"],
                    'aeropuerto_origen':{
                        'nombre':datos["data"]["attributes"]["from_airport"]["name"],
                        'ciudad':datos["data"]["attributes"]["from_airport"]["city"],
                        'codigo':aeropuerto_origen
                    },
                    'aeropuerto_destino':{
                        'nombre':datos["data"]["attributes"]["to_airport"]["name"],
                        'ciudad':datos["data"]["attributes"]["to_airport"]["name"],
                        'codigo':aeropuerto_destino
                    },
                    "distancia_km":datos["data"]["attributes"]["kilometers"],
                    "distancia_millas":datos["data"]["attributes"]["miles"],
                    "distancia_millas_nauticas":datos["data"]["attributes"]["nautical_miles"]
                }
                return JsonResponse(result_data)
            elif response_post.status_code == 422:
                return JsonResponse({
                    "success":False,
                    "error":"uno o ambo codigo son invalidos"
                })
            else:
                return JsonResponse({
                    "success": False,
                    "error": f"Error den la api: {response_post.status_code}"
                })
        except request.exceptions.Timeout:
            return JsonResponse({
                "success":False,
                "error": "Tiempo de espera agotado. intente nuevamente."
            })
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                "success":False,
                "error": "Error de conexion. verifique su conexion a internet."
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error":f"Error insperado: {str(e)}"
            })
    return JsonResponse({
            "success":False,
            "error": "Método no permitido"
        })
