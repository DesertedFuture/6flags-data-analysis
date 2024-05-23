import requests


def api_call(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.status_code)


def print_clean(data):
    for land in data['lands']:
        for ride in land['rides']:
            print(ride)


def clean_input(api_response):
    cleaned_data = []
    for land in api_response['lands']:
        land_id = land['id']
        for ride in land['rides']:
            cleaned_data.append((
                land_id,
                ride['id'],
                ride['name'],
                ride['is_open'],
                ride['wait_time'],
                ride['last_updated']
                ))
    return cleaned_data
