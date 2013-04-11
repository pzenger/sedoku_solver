import os

os.system('python timing.py sudoku2sat.py satisfiable/size9')
os.system('python timing.py sudoku2sat.py satisfiable/size16')
os.system('python timing.py sudoku2sat.py satisfiable/size25')

os.system('python timing.py sudoku2sat.py hard_online')

os.system('python timing.py sudoku2sat.py generated/size9/20%')
os.system('python timing.py sudoku2sat.py generated/size16/20%')
os.system('python timing.py sudoku2sat.py generated/size25/20%')