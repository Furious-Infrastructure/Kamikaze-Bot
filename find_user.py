from core.auth.users import *

u = User()
user_info = u.find("2342342422342")

print("====================================")
print(f"Username: {user_info.username}")
print(f"UserID: {user_info.userid}")
print(f"Max Concurrents: {user_info.max_con}")
print(f"Max Time: {user_info.max_time}")
print(f"Cooldown: {user_info.cooldown}")
print(f"Mod Level: {user_info.mod_level}")
print("=====================================")