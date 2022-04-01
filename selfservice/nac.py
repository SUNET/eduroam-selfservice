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

        try:
            res = requests.get(
                self.url + f"/{username}", headers=self.headers).json()
        except Exception:
            errors.append('Connection to NAC server failed')
            return errors

        if "data" not in res:
            errors.append("Could not contact NAC server")

        if len(res["data"]) == 0:
            create_user = True

        if create_user:
            userdata = {
                "username": username,
                "password": password,
                "vlan": 700,
                "active": True
            }

            try:
                res = requests.post(
                    self.url, headers=self.headers, json=userdata)

                if res.status_code != 200:
                    errors.append("Failed to create user")
            except Exception:
                errors.append("Failed to handle request")
        else:
            userdata = {
                "password": password,
                "vlan": 700,
                "active": True
            }

            try:
                res = requests.put(
                    self.url + f"/{username}", headers=self.headers,
                    json=userdata)

            except Exception:
                errors.append("Failed to handle request")
                return errors

            if res.status_code != 200:
                errors.append("Failed to change password for user")

        return errors
