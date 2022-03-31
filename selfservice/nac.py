import requests


class NacConnection(object):
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def handle_user(self, username, password):
        errors = []
        create_user = False

        res = requests.get(
            self.url + f"/{username}", headers=self.headers)
        res_json = res.json()

        if "data" not in res_json:
            errors.append("Could not contact NAC server")

        if len(res_json["data"]) == 0:
            create_user = True

        try:
            if create_user:
                userdata = {
                    "username": username,
                    "password": password,
                    "vlan": 700,
                    "active": True
                }

                res = requests.post(
                    self.url, headers=self.headers, json=userdata)

                if res.status_code != 200:
                    errors.append("Failed to create user")
            else:
                userdata = {
                    "password": password,
                    "vlan": 700,
                    "active": True
                }

                res = requests.put(
                    self.url + f"/{username}", headers=self.headers,
                    json=userdata)

                if res.status_code != 200:
                    errors.append("Failed to change password for user")
        except Exception:
            errors.append("Failed to handle request")

        return errors
