#CORDIC algo to compute sine/cos/tan using posit type

import math
import softposit as sp
import sfpy as sf

#function to return value of Ki
def val_Ki(n):
    Ki =  sp.posit32(1 / math.sqrt(1 + 2**(-2*n)))
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
        table[2**(-i)] = sp.posit32(math.degrees(math.atan(2**(-i))))
    return table

#function for computing the cordic iteration
def cordic_itr(ang, n):
    z = sp.posit32(ang)
    x = sp.posit32(1 / val_An(n))
    y = sp.posit32(0.0)
    di = 0
    arctan_table = atan_table(n)
   
    #iterate cordic algorithm
    for i in range(n+1):
        rot_ang = arctan_table[2**(-i)]
        if z >= 0:
            di = 1
        else:
            di = -1
        
        x_prime = x - y * di * 2**(-i)
        y_prime = y + x * di * 2**(-i)
        z_prime = z - di * rot_ang
        
        #verification table - check that the iteration is correct
        #print(i, 2.0**(-i), rot_ang, z, rot_ang, z_prime)

        x = x_prime
        y = y_prime
        z = z_prime

    print("cos of angle (in degrees) = ", x)
    print("sin of angle (in degrees) = ", y)
    print("tan of angle (in degrees) = ", y/x)
   
    #verify angle is correct
    print("angle = ", math.degrees(math.atan(y/x)))


##### TEST #####

#k = val_Ki(1)
#a = val_An(1)
#table = atan_table(20)
#print(2.0**(-5), table[2.0**(-5)], '\n')
#print(table)

#print("posit: ", sp.posit32(1 / math.sqrt(1 + 2**(-2*0))))
#print("float: ", float(1 / math.sqrt(1 + 2**(-2*0))))


cordic_itr(20, 40)




