import os
os.system('g++ -shared -I "C:/Program Files/Python36/include" -std=c++11 ./audio/cpplib.cpp "C:/Program Files/Python36/libs/libpython36.a" -o ./audio/cpplib.pyd')
