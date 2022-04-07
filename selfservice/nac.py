import requests


class NacConnection(object):
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

    def handle_user(self, username, password):
        errors = []
        create_user = False
        userdata = {"password": password, "vlan": 700, "active": True}

        try:
            res = requests.get(
                self.url + f"/{username}", headers=self.headers, timeout=10
            ).json()

            if "data" not in res:
                errors.append("Could not contact NAC server")
            if len(res["data"]) == 0:
                create_user = True
            if create_user:
                userdata["username"] = username
                res = requests.post(
                    self.url, headers=self.headers, json=userdata, timeout=10
                )

                if res.status_code != 200:
                    errors.append("Failed to create user")
            else:
                res = requests.put(
                    self.url + f"/{username}", headers=self.headers,
                    json=userdata
                )

                if res.status_code != 200:
                    errors.append("Failed to change password for user")
        except Exception:
            errors.append("Failed to handle request")

        return errors
