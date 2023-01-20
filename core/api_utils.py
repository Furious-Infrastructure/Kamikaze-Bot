import os, json

class API_Info:
    name: str
    url: str
    max_time: int
    max_boot: int
    cooldown: int
    method: list

class API():
    apis_found: list[API_Info]
    def __init__(self, m: str) -> None:
        self.apis_found = []
        self.method = m
        self.__look_for_api()

    def __look_for_api(self) -> None:
        api_i = API_Info()

        if not os.path.isfile("assets/apis.json"): return
        api_db = open("assets/apis.json")
        apis = json.loads(api_db.read())

        for api in apis:

            api_i.name = api
            api_i.url = apis[api]['url']
            api_i.max_time = apis[api]['max_time']
            api_i.max_boot = apis[api]['max_boot']
            api_i.cooldown = apis[api]['cooldown']
            api_i.methods = apis[api]['methods']
            self.apis_found.append(api_i)
            
        api_db.close()

    def check_for_apis(self) -> bool:
        if len(self.apis_found) > 0: return True
        return False

    def count_apis_found(self) -> int:
        return len(self.apis_found)
    
    """
    [
        <__main__.API_Info object at 0x7f81290c7d30>,
        <__main__.API_Info object at 0x7f81290c7d30>
    ]
    """
    def get_apis(self) -> list[API_Info]:
        return self.apis_found

a = API("UDP") # Call 'API' class
api_check = a.check_for_apis() # Returns a boolean if apis with method is found in API Config file
api_count = a.count_apis_found() # Returns an interger count of apis with method found in API Config file

apis = a.get_apis()
print(apis)

for i in apis:
    print(i.name)
    print(i.url)