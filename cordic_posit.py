#CORDIC algo to compute sine/cos/tan using posit type

import math
import csv
import softposit as sp
import bigfloat as bf
PREC = 1000

#function to convert degrees to radians
def deg_to_rad(angle):
    return angle * math.pi / 180

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
    
    print("\nPosit representation:")
    print("cos of %d (in degrees) = %.200f" %(ang, x))
    print("sin of %d (in degrees) = %.200f" %(ang, y))
    print("tan of %d (in degrees) = %.200f" %(ang, y/x))
    
    print("\nMathlib representation:")
    print("cos of %d (in degrees) = %.200f" %(ang, math.cos(deg_to_rad(ang))))
    print("sin of %d (in degrees) = %.200f" %(ang, math.sin(deg_to_rad(ang))))
    print("tan of %d (in degrees) = %.200f" %(ang, math.tan(deg_to_rad(ang))))

    print("\nMPFR representation:")
    print("cos of %d (in degrees) = " %ang, bf.cos(deg_to_rad(ang), bf.precision(PREC)))
    print("sin of %d (in degrees) = " %ang, bf.sin(deg_to_rad(ang), bf.precision(PREC)))
    print("tan of %d (in degrees) = " %ang, bf.tan(deg_to_rad(ang), bf.precision(PREC)))
    
    swap = float(x) 
    swap = float(x) 
    swap = float(x) 
    x_pp = bf.BigFloat.exact(swap)
    #print("bigfloat exact: ", swap, x_pp)
    x_mpfr = bf.cos((math.pi/9), bf.precision(PREC))
    y_mpfr = bf.sin((math.pi/9), bf.precision(PREC))
    z_mpfr = bf.tan((math.pi/9), bf.precision(PREC))

    #print("error of cos of %d (in degrees) = %.200f" %(ang, x_mpfr-x_pp))
    #print("error of sin of %d (in degrees) = %.200f" %(ang, y_mpfr-y))
    #print("error of tan of %d (in degrees) = %.200f" %(ang, z_mpfr-z))
    

    #verify angle is correct
    #print("angle = ", math.degrees(math.atan(y/x)))
    
    arr1 = [ang, "%.200f" %x, "%.200f" %y_mpfr, "%.200f" %x, "%.200f" %x, "%.200f" %x, "%.200f"
            %x,"%.200f" %x,"%.200f" %x,"%.200f" %x,"%.200f" %x,"%.200f" %x,"%.200f"
            %x, "%.200f" %x, "%.200f" %x,]

    with open('posit.csv', 'a') as f:
        #f.write("%.200f\n" % x) 
        csvfile = csv.writer(f)
        csvfile.writerow(arr1)

##### Main Program #####

if __name__ == '__main__':
    fields = ['Angle', 'Posit-sin', 'Error', 'Posit-cos', 'Error', 'Posit-tan', 'Error', 'Float-sin',
            'Error', 'Float-cos', 'Error', 'Float-tan', 'Error', 'Mathlib', 'MPFR']

    with open('posit.csv', 'w') as f:
            csvfile = csv.writer(f)
            csvfile.writerow(fields)

    cordic_itr(20, 40)
    cordic_itr(20, 40)
    cordic_itr(20, 40)

    f.close()




