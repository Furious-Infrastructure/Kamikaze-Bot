import json

class Plans:
    def __init__(self) -> None:
        self.data = json.loads(open("assets/plans.json").read())
        
    def Plan_info(self):
        self.basic_plan = self.data["Basic"]
        self.basic_time = self.basic_plan["maxtime"]
        self.basic_cons = self.basic_plan["concurrents"]
        self.basic_cooldown = self.basic_plan["cooldown"]
        self.basic_price = self.basic_plan["price"]

        self.standard_plan = self.data["Standard"]
        self.standard_time = self.standard_plan["Maxtime"]
        self.standard_cons = self.standard_plan["Concurrents"]
        self.standard_cooldown = self.standard_plan["Cooldown"]
        self.standard_price = self.standard_plan["prices"]

        self.premium_plan = self.data["VIP"]
        self.premium_time = self.premium_plan["maxtime"]
        self.premium_raw_maxtime = self.premium_plan["raw_maxtime"]
        self.premium_cons = self.premium_plan["concurrents"]
        self.premium_cooldown = self.premium_plan["Cooldowm"]
        self.premium_price = self.data["prices"]