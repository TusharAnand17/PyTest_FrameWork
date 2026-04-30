import requests

class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        return requests.get(self.base_url + endpoint)

    def post(self, endpoint, payload):
        return requests.post(self.base_url + endpoint, json=payload)