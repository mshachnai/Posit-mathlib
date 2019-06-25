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
    print("cos of %d (in degrees) = %.30f" %(ang, x))
    print("sin of %d (in degrees) = %.30f" %(ang, y))
    print("tan of %d (in degrees) = %.30f" %(ang, y/x))
    
    print("\nMathlib representation:")
    print("cos of %d (in degrees) = %.30f" %(ang, math.cos(deg_to_rad(ang))))
    print("sin of %d (in degrees) = %.30f" %(ang, math.sin(deg_to_rad(ang))))
    print("tan of %d (in degrees) = %.30f" %(ang, math.tan(deg_to_rad(ang))))

    print("\nMPFR representation:")
    print("cos of %d (in degrees) = " %ang, bf.cos(deg_to_rad(ang), bf.precision(PREC)))
    print("sin of %d (in degrees) = " %ang, bf.sin(deg_to_rad(ang), bf.precision(PREC)))
    print("tan of %d (in degrees) = " %ang, bf.tan(deg_to_rad(ang), bf.precision(PREC)))
    
    swapx = float(x) 
    swapy = float(y) 
    swaptan = float(y/x) 
    cos_p = bf.BigFloat.exact(swapx)
    sin_p = bf.BigFloat.exact(swapy)
    tan_p = bf.BigFloat.exact(swaptan)
    #print("bigfloat exact: ", swap, x_pp)

    cos_mpfr = bf.cos(deg_to_rad(ang), bf.precision(PREC))
    sin_mpfr = bf.sin(deg_to_rad(ang), bf.precision(PREC))
    tan_mpfr = bf.tan(deg_to_rad(ang), bf.precision(PREC))
    
    cos_diff = (cos_mpfr-cos_p) / cos_mpfr
    sin_diff = (sin_mpfr-sin_p) / sin_mpfr
    tan_diff = (tan_mpfr-tan_p) / tan_mpfr
    #print("error of cos of %d (in degrees) = %.200f" %(ang, x_mpfr-x_pp))
    #print("error of sin of %d (in degrees) = %.200f" %(ang, y_mpfr-y))
    #print("error of tan of %d (in degrees) = %.200f" %(ang, z_mpfr-z))
    

    #verify angle is correct
    #print("angle = ", math.degrees(math.atan(y/x)))
    
    arr1 = [ang, "%.100f" %y, "%.100f" %sin_mpfr ,"%.100f" %sin_diff, "%.100f" %x,
            "%.100f" %cos_mpfr, "%.100f" %cos_diff,
            "%.100f" %(y/x), "%.100f" %tan_mpfr, "%.100f" %tan_diff] 
            
            #"%.100f" %x,"%.100f" %x,"%.100f"
            #%x, "%.100f" %x, "%.100f" %x,]

    arr2 = [ang, "%.40E" %y, "%.40E" %sin_mpfr ,"%.40E" %sin_diff, "%.40E" %x,
            "%.40E" %cos_mpfr, "%.40E" %cos_diff,
            "%.40E" %(y/x), "%.40E" %tan_mpfr, "%.40E" %tan_diff] 

            #"%.40E" %x,"%.40E" %x,"%.40E"
            #%x, "%.40E" %x, "%.40E" %x,]

    with open('posit.csv', 'a') as f:
        csvfile = csv.writer(f)
        csvfile.writerow(arr1)

    with open('posit_Expform.csv', 'a') as f1:
        csvfile = csv.writer(f1)
        csvfile.writerow(arr2)


##### Main Program #####

if __name__ == '__main__':
    fields = ['Angle', 'Posit-sin', 'MPFR-sin', 'Error', 'Posit-cos', 'MPFR-cos',
            'Error', 'Posit-tan',  'MPFR-tan','Error']
    #'Float-sin', 'Error', 'Float-cos', 'Error', 'Float-tan', 'Error', 
    #        'Mathlib-sin', 'Mathlib-cos', 'Mathlib-tan']

    with open('posit.csv', 'w') as f:
            csvfile = csv.writer(f)
            csvfile.writerow(fields)

    with open('posit_Expform.csv', 'w') as f1:
            csvfile = csv.writer(f1)
            csvfile.writerow(fields)

    for i in range(361):
        cordic_itr(i, 45)

    f.close()




