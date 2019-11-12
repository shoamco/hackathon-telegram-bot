import requests


def geocode(name):
    param ='%20'.join(name.split(' '))
    r = requests.get(f"https://nominatim.openstreetmap.org/search?q={param}&format=json")
    r.raise_for_status()  # will raise an exception for HTTp status code != 200
    data = r.json()
    if len(data) == 0:
        raise Exception(f"I don't know any{name}")
    element = data[0]
    print(element)
    return tuple([float(element['lat']), float(element['lon'])])