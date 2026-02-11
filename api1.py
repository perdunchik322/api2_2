import requests

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
point = input()

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": point,
    "kind": "metro",
    "results": 1,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
data = response.json()

metro_name = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["name"]
print(metro_name)
