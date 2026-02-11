def get_size(json_response, padding=1.1):
    envelope = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"][
        "Envelope"]
    lower_corner = list(map(float, envelope["lowerCorner"].split()))
    upper_corner = list(map(float, envelope["upperCorner"].split()))
    spn_x = (upper_corner[0] - lower_corner[0]) / 2 * padding
    spn_y = (upper_corner[1] - lower_corner[1]) / 2 * padding
    min_spn = 0.001
    spn_x = max(spn_x, min_spn)
    spn_y = max(spn_y, min_spn)
    return f"{spn_x},{spn_y}"
