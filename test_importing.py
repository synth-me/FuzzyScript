import cloi7u
from cloi7u import file_read,interpreter
import os 

class funcc():

   def funcc(x):
       list_ = ['a','b','c']
       try:
           if x in list_:
               return list_.index(x)
           else:
               return 0
       except:
           return 0 

class funcc_2():
    def funcc_2(x):
       list_ = ['q','a','b','c']
       try:
           if x in list_:
               return list_.index(x)
           else:
               return 'testing'
       except:
           return 0



def file_name():
    x = os.path.realpath(__file__)
    y = x.split("\\")
    y_ = y[len(y)-1].split('.py')
    return y_[0] 

f = file_read.read('/Users/murie/OneDrive/Área de Trabalho/cloudy/set.txt')
p = interpreter.run(f,path=file_name())
print(p)

