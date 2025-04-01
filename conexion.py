from requests_oauthlib import OAuth1
import requests

# Tus credenciales de API
consumer_key = "323d77a2801c4cb290c67c207a28f3a5"
consumer_secret = "4446f6b14ac544aab3acdc7776df7d8a"

# Inicializamos OAuth1 con nuestras credenciales
auth = OAuth1(consumer_key, consumer_secret)

# URL para obtener la información del usuario
url = "https://platform.fatsecret.com/rest/server.api"

# Parámetros para la solicitud
params = {
    "method": "users.get_current_user",
    "format": "json",
    "language": "es"
}

# Hacemos la solicitud
response = requests.get(url, params=params, auth=auth)

# Verificamos si la respuesta fue exitosa
if response.status_code == 200:
    user_info = response.json()
    print("✅ Credenciales válidas.")
    print("Información del usuario:", user_info)
else:
    print("❌ Error al verificar las credenciales:", response.status_code)