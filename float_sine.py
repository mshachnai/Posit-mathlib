#sine function using float point and CORDIC algo

import math

#print(math.sin(math.pi/4))

#function to return value of Ki (cordic gain) 
def val_Ki(n):
    Ki = 1.0 / math.sqrt(2)
    for i in range (1, n):
        Ki = Ki * (1 / math.sqrt(1 + 2**(-2*i)))
    return Ki


#function to return a dictionary (tan:arctan) of arctan values up to n
def atan_table(n):
    table = {}
    for i in range(n):
        table[2**(-i)] = math.degrees(math.atan(2**(-i)))
    return table

k = val_Ki(20)
table = atan_table(20)
#print(table)
print(k)




