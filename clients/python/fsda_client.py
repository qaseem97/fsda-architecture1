import requests

class FSDA:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def __getattr__(self, func_name):
        def method(*args):
            r = requests.post(f"{self.base_url}/call/{func_name}", json={"args": list(args)})
            if r.status_code != 200:
                raise Exception(r.json().get("detail", "Unknown error"))
            return r.json()["result"]
        return method