import sys
from io import BytesIO
import requests
from PIL import Image
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
    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "ll": address_ll,
        "text": "аптека",
        "lang": "ru_RU",
        "type": "biz",
        "results": 10
    }

    search_response = requests.get(search_api_server, params=search_params)
    search_response_json = search_response.json()
    organizations = search_response_json["features"]

    points = []

    for org in organizations:
        try:
            org_coords = org["geometry"]["coordinates"]
            org_point = (org_coords[0], org_coords[1])
            distance = lonlat_distance(target_point, org_point)
            org_name = org["properties"]["CompanyMetaData"]["name"]
            org_address = org["properties"]["CompanyMetaData"]["address"]
            hours = org["properties"]["CompanyMetaData"].get("Hours", {}).get("text", "")
            points.append([org_name, org_point, org_address, hours, distance])
        except:
            continue

    if not points:
        print("Аптеки не найдены")
        return

    points.sort(key=lambda x: x[4])
    points = points[:10]

    pt_marks = [f"{lon},{lat},pm2rdm"]

    for org in points:
        org_name = org[0]
        org_lon, org_lat = org[1]
        org_address = org[2]
        hours = org[3]
        distance_km = org[4] / 1000

        if not hours:
            color = "pm2grm"
        elif "круглосуточ" in hours.lower():
            color = "pm2gnm"
        else:
            color = "pm2blm"

        pt_marks.append(f"{org_lon},{org_lat},{color}")

        print(f"Название: {org_name}")
        print(f"Адрес: {org_address}")
        print(f"Время работы: {hours if hours else 'Не указано'}")
        print(f"Расстояние: {distance_km:.1f} км")
        print()

    map_api_server = "https://static-maps.yandex.ru/1.x/"
    map_params = {
        "l": "map",
        "pt": "~".join(pt_marks)
    }

    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).show()


apteka_data_photo()
