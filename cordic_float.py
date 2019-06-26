#CORDIC algo to compute sine/cos/tan using IEEE floating point

import math
import csv

#function to convert degrees to radians
def deg_to_rad(angle):
    return angle * math.pi / 180

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
        
        #verification table - to check if iteration is correct
        #print(i, 2.0**(-i), rot_ang, z, rot_ang, z_prime)

        x = x_prime
        y = y_prime
        z = z_prime

    print("\nIEEE Float representation:")
    print("cos of %d (in degrees) = " %ang, x)
    print("sin of %d (in degrees) = " %ang, y)
    print("tan of %d (in degrees) = "%ang, y/x)
    
    print("\nMathlib representation:")
    print("cos of %d (in degrees) = " %ang, math.cos(math.pi/9))
    print("sin of %d (in degrees) = " %ang, math.sin(math.pi/9))
    print("tan of %d (in degrees) = " %ang, math.tan(math.pi/9))

    #verify angle is correct
    print("angle = ", math.degrees(math.atan(y/x)))


##### TEST #####

if __name__ == '__main__':
    cordic_itr(i, 45)

    #for i in range(361):
    #    cordic_itr(i, 45)

#    f.close()



