from core.plan_utils import *

p = Plans()

print(p.find_plan(0).name, end=": ")
print(f"{p.find_plan(0).maxtime}")

print(p.find_plan("VIP").name, end=": ")
print(str(p.find_plan("VIP").maxtime))