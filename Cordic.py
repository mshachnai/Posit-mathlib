#CORDIC algo to compute sine/cos/tan (includes posit and float)

import math
import csv
import softposit as sp
import bigfloat as bf
PREC = 1000

#function to convert degrees to radians
def deg_to_rad(angle):
    return angle * math.pi / 180

###### FLOAT FUNCTIONS #####
#function to return value of Ki
def val_Kif(n):
    Ki =  1 / math.sqrt(1 + 2**(-2*n))
    return Ki

#function to return value of An (cordic gain) 
def val_Anf(n):
    An = math.sqrt(2)
    for i in range (1, n):
        An = An * math.sqrt(1 + 2**(-2*i))
    return An

#function to return a dictionary (tan:arctan) of arctan values 
def atan_tablef(n):
    table = {}
    for i in range(n+1):
        table[2**(-i)] = math.degrees(math.atan(2**(-i)))
    return table


###### POSIT FUNCTIONS #####
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


### CORDIC FUNCTION ###
#function for computing the cordic iteration
def cordic_itr(ang, n):
    #posit vars
    z = sp.posit32(ang)
    x = sp.posit32(1 / val_An(n))
    y = sp.posit32(0.0)
    di = 0
    arctan_table = atan_table(n)
   
    #float vars
    zf = float(ang)
    xf = float(1.0 / val_Anf(n))
    yf = float(0.0)
    arctan_tablef = atan_tablef(n)
    
    #iterate cordic algorithm
    for i in range(n+1):
        rot_ang = arctan_table[2**(-i)]
        rot_angf = arctan_tablef[2**(-i)]
        if z >= 0:
            di = 1
        else:
            di = -1

        x_prime = x - y * di * 2**(-i)
        y_prime = y + x * di * 2**(-i)
        z_prime = z - di * rot_ang
        xf_prime = float(xf - yf * di * 2.0**(-i))
        yf_prime = float(yf + xf * di * 2.0**(-i))
        zf_prime = float(zf - di * rot_angf)
        
        #verification table - check that the iteration is correct
        #print(i, 2.0**(-i), rot_ang, z, rot_ang, z_prime)

        x = x_prime
        y = y_prime
        z = z_prime
        xf = xf_prime
        yf = yf_prime
        zf = zf_prime
    """
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
    """
    #posit and mpfr output vars
    swapx = float(x) 
    swapy = float(y) 
    swaptan = float(y/x) 
    cos_p = bf.BigFloat.exact(swapx)
    sin_p = bf.BigFloat.exact(swapy)
    tan_p = bf.BigFloat.exact(swaptan)

    cos_mpfr = bf.cos(deg_to_rad(ang), bf.precision(PREC))
    sin_mpfr = bf.sin(deg_to_rad(ang), bf.precision(PREC))
    tan_mpfr = bf.tan(deg_to_rad(ang), bf.precision(PREC))
     
    cos_diff = (cos_mpfr-cos_p) / cos_mpfr
    sin_diff = (sin_mpfr-sin_p) / sin_mpfr
    tan_diff = (tan_mpfr-tan_p) / tan_mpfr
     
    #float and mathlib output vars
    cos_mlib = float(math.cos(ang))
    sin_mlib = float(math.sin(ang))
    tan_mlib = float(math.tan(ang))
    
    try:
        cos_fdiff = (cos_mlib-xf) / cos_mlib
    except ZeroDivisionError:
        cos_fdiff = float('Inf')
    try:
        sin_fdiff = (sin_mlib-yf) / sin_mlib
    except ZeroDivisionError:
        sin_fdiff = float('Inf')
    try:
        tan_fdiff = (tan_mlib-yf/xf) / tan_mlib
    except ZeroDivisionError:
        tan_fdiff = float('Inf')
        

    arr1 = [ang,
            #posit
            "%.100f" %y, "%.100f" %sin_mpfr ,"%.100f" %sin_diff, "%.100f" %x,
            "%.100f" %cos_mpfr, "%.100f" %cos_diff,
            "%.100f" %(y/x), "%.100f" %tan_mpfr, "%.100f" %tan_diff, 
            #float 
            "%.100f" %yf, "%.100f" %sin_mlib ,"%.100f" %sin_fdiff, "%.100f" %xf,
            "%.100f" %cos_mlib, "%.100f" %cos_fdiff,
            "%.100f" %(yf/xf), "%.100f" %tan_mlib, "%.100f" %tan_fdiff] 
            
    arr2 = [ang,
            #posit
            "%.20E" %y, "%.20E" %sin_mpfr ,"%.20E" %sin_diff, "%.20E" %x,
            "%.20E" %cos_mpfr, "%.20E" %cos_diff,
            "%.20E" %(y/x), "%.20E" %tan_mpfr, "%.20E" %tan_diff, 
            #float 
            "%.20E" %yf, "%.20E" %sin_mlib ,"%.20E" %sin_fdiff, "%.20E" %xf,
            "%.20E" %cos_mlib, "%.20E" %cos_fdiff,
            "%.20E" %(yf/xf), "%.20E" %tan_mlib, "%.20E" %tan_fdiff] 

    with open('posit.csv', 'a') as f:
        csvfile = csv.writer(f)
        csvfile.writerow(arr1)

    with open('posit_Expform.csv', 'a') as f1:
        csvfile = csv.writer(f1)
        csvfile.writerow(arr2)


##### Main Program #####

if __name__ == '__main__':
    fields = ['Angle',
            #posit
            'Posit-sin', 'MPFR-sin', 'Error', 'Posit-cos', 'MPFR-cos','Error',
            'Posit-tan', 'MPFR-tan', 'Error',
            #float
            'Float-sin', 'Mathlib-sin', 'Error', 'Float-cos', 'Mathlib-cos', 'Error',
            'Float-tan', 'Mathlib-tan', 'Error']

    with open('posit.csv', 'w') as f:
            csvfile = csv.writer(f)
            csvfile.writerow(fields)

    with open('posit_Expform.csv', 'w') as f1:
            csvfile = csv.writer(f1)
            csvfile.writerow(fields)

    for i in range(361):
        cordic_itr(i, 45)

    f.close()




