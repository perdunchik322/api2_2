import sys
from io import BytesIO
import requests
from PIL import Image
import json

from get_distance import lonlat_distance


def apteka_data_photo():
    toponym_to_find = " ".join(sys.argv[1:])

    geocoder_api_server = "https://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    lon, lat = toponym["Point"]["pos"].split()
    address_ll = f"{lon},{lat}"
    target_point = (float(lon), float(lat))

    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "ll": address_ll,
        "text": "аптека",
        "lang": "ru_RU",
        "type": "biz"
    }

    search_response = requests.get(search_api_server, params=search_params)
    search_response_json = search_response.json()

    organizations = search_response_json["features"]

    min_distance = float('inf')
    nearest_org = None

    for org in organizations:
        try:
            org_coords = org["geometry"]["coordinates"]
            org_point = (org_coords[0], org_coords[1])
            distance = lonlat_distance(target_point, org_point)

            if distance < min_distance:
                min_distance = distance
                nearest_org = org
        except:
            continue

    if not nearest_org:
        print("Аптеки не найдены")
        return

    org_name = nearest_org["properties"]["CompanyMetaData"]["name"]
    org_address = nearest_org["properties"]["CompanyMetaData"]["address"]
    time_of_working = nearest_org["properties"]["CompanyMetaData"].get("Hours", {}).get("text", "Не указано")
    distance_km = min_distance / 1000

    print(f"Название: {org_name}")
    print(f"Адрес: {org_address}")
    print(f"Время работы: {time_of_working}")
    print(f"Расстояние: {distance_km:.1f} км")

    org_point_coords = nearest_org["geometry"]["coordinates"]
    org_point = f"{org_point_coords[0]},{org_point_coords[1]}"

    map_api_server = "https://static-maps.yandex.ru/1.x/"
    map_params = {
        "l": "map",
        "pt": f"{lon},{lat},ya_en~{org_point},pm2gnm",
    }

    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).show()

apteka_data_photo()