import os

os.system('python timing.py enfragmo.py satisfiable/size9')
os.system('python timing.py enfragmo.py satisfiable/size16')
os.system('python timing.py enfragmo.py satisfiable/size25')

os.system('python timing.py enfragmo.py hard_online')

os.system('python timing.py enfragmo.py generated/size9/20%')
os.system('python timing.py enfragmo.py generated/size16/20%')
os.system('python timing.py enfragmo.py generated/size25/20%')

os.system('python timing.py enfragmo.py generated/size9/40%')
os.system('python timing.py enfragmo.py generated/size16/40%')
os.system('python timing.py enfragmo.py generated/size25/40%')