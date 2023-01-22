import json


"""
    Example Use:
    
plans = Plans()
for i in plans.get_plans():
    print(f"Plan: {i.name}")
"""
class Plan_Info:
    name: str
    maxtime: int
    raw_maxtime: int
    concurrents: int
    cooldown: int
    price: int

def setPlanInfo(nm: str, m: int, r: int, c: int, cd: int, p: int) -> Plan_Info:
    n = Plan_Info()
    n.name = nm
    n.maxtime = m
    n.raw_maxtime = r
    n.concurrents = c
    n.cooldown = cd
    n.price = p
    return n

class Plans():
    """
        {
            "PLAN_NAME": [
                < class PLAN_INFO >
                < class PLAN_INFO >
                < class PLAN_INFO >
                ]
        }
    """
    __plans_found: list[Plan_Info]

    def __init__(self) -> None:
        self.__plans_found = []
        self.data = self.updateJSON()
        self.__dict2object()  

    def updateJSON(self) -> str:
        planFile = open("assets/plans.json")
        data = planFile.read()
        planFile.close()
        return json.loads(data)
        
    def __dict2object(self) -> None:
        plan = Plan_Info()

        for structure in self.data:
                plan = setPlanInfo(structure, self.data[structure]['maxtime'], self.data[structure]['raw_maxtime'], self.data[structure]['concurrents'], self.data[structure]['cooldown'], self.data[structure]['price'])
                self.__plans_found.append(plan)
    
    def find_plan(self, name_or_num: str|int) -> Plan_Info:
        if type(name_or_num) == str:
            return self.__plans_found[name_or_num]
        elif type(name_or_num) == int:
            c = 0
            for structure in self.data:
                if c == name_or_num:
                    return setPlanInfo(structure, self.data[structure]['maxtime'], self.data[structure]['raw_maxtime'], self.data[structure]['concurrent'], self.data[structure]['cooldown'], self.data[structure]['price'])
                c+=1

        return setPlanInfo("", 0, 0, 0, 0, 0)

    def count_plans(self) -> int:
        return len(self.__plans_found)

    def get_plans(self) -> dict[Plan_Info]:
        return self.__plans_found
