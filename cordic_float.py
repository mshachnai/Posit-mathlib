#CORDIC algo to compute sine/cos/tan using IEEE floating point

import math


#function to return value of Ki
def val_Ki(n):
    Ki =  1 / math.sqrt(1 + 2**(-2*n))
    return Ki

#function to return value of An (cordic gain) 
def val_An(n):
    An = math.sqrt(2)
    for i in range (1, n):
        An = An * math.sqrt(1 + 2**(-2*i))
    return An

#function to return a dictionary (tan:arctan) of arctan values 
def atan_table(n):
    table = {}
    for i in range(n+1):
        table[2**(-i)] = math.degrees(math.atan(2**(-i)))
    return table

#function for computing the cordic iteration
def cordic_itr(ang, n):
    z = float(ang)
    x = 1.0 / val_An(n)
    y = 0.0
    di = 0
    arctan_table = atan_table(n)
    
    #iterate cordic algorithm
    for i in range(n+1):
        rot_ang = arctan_table[2**(-i)]
        if z >= 0:
            di = 1
        else:
            di = -1
        
        x_prime = x - y * di * 2.0**(-i)
        y_prime = y + x * di * 2.0**(-i)
        z_prime = z - di * rot_ang
        
        print(i, 2.0**(-i), rot_ang, z, rot_ang, z_prime)

        x = x_prime
        y = y_prime
        z = z_prime

    print("cos of angle = ", x)
    print("sin of angle = ", y)
    print("tan of angle = ", y/x)
   
    #verify numbers are correct
    print("angle = ", math.degrees(math.atan(y/x)))


##### TEST #####

#k = val_Ki(1)
#a = val_An(1)
#table = atan_table(20)
#print(2.0**(-5), table[2.0**(-5)], '\n')
#print(table)

cordic_itr(20, 40)




