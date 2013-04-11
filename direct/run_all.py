import os


# Run all on hard 9x9 boards
#os.system('python timing.py solver_1.py hard_online')
#os.system('python timing.py solver_2.py hard_online')
#os.system('python timing.py solver_3.py hard_online')


# 9 with slow
#os.system('python timing.py solver_1.py generated/size9/20%')
#os.system('python timing.py solver_1.py generated/size9/40%')


# 9 and 16 with med solver
#os.system('python timing.py solver_2.py generated/size9/20%')
#os.system('python timing.py solver_2.py generated/size9/40%')
#os.system('python timing.py solver_2.py generated/size16/20%')
#os.system('python timing.py solver_2.py generated/size16/40%')

# 9 and 16 with fast solver
#os.system('python timing.py solver_3.py generated/size9/20%')
#os.system('python timing.py solver_3.py generated/size9/40%')
#os.system('python timing.py solver_3.py generated/size16/20%')
#os.system('python timing.py solver_3.py generated/size16/40%')


# 25 with fastest 2 solvers, only 40% with fastest
os.system('python timing.py solver_2.py generated/size25/20%')
os.system('python timing.py solver_3.py generated/size25/20%')
#os.system('python timing.py solver_3.py generated/size25/40%')

# a 36 with fastest
os.system('python timing.py solver_3.py generated/size36/20%')
#os.system('python timing.py solver_3.py generated/size36/40%')

# 16 with slow
os.system('python timing.py solver_1.py generated/size16/20%')
#os.system('python timing.py solver_1.py generated/size16/40%')

# Just incase it manages to get this far:
os.system('python timing.py solver_2.py generated/size36/20%')
#os.system('python timing.py solver_2.py generated/size36/40%')




