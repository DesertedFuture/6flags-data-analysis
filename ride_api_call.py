import requests


class APIClient:
    def __init__(self, api_url):
        self.url = api_url

    def api_call(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            print("api call successful")
            return data
        else:
            print(response.status_code)

    def print_clean(self, data):
        for land in data['lands']:
            for ride in land['rides']:
                print(ride)

    def clean_input(self, api_response):
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
        print("data cleaned for insertion")
        return cleaned_data
