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

#function to return value of An (cordic gain) for trig functions 
def val_An(n):
    An = math.sqrt(2)
    for i in range (1, n):
        An = An * math.sqrt(1 + 2**(-2*i))
    return An

#function to return value of An (cordic gain) for hyperbolic functions 
def val_hyp_An(n):
    An = math.sqrt(.75)
    print(An)
    for i in range (2, n):
        An = An * math.sqrt(1 - 2**(-2*sigma_hyper(i)))
    print(An)
    return An

#function to return a dictionary (tan:arctan) of arctan values 
def atan_table(n):
    table = {}
    for i in range(n+1):
        table[2**(-i)] = sp.posit32(math.degrees(math.atan(2**(-i))))
    return table

#function to return a dictionary of arctanh values 
def atanh_table(n):
    table = {}
    for i in range(n+1):
        table[2**(-sigma_hyper(i))] = sp.posit32(math.atanh(2**(-sigma_hyper(i))))
    return table

#function to compute sigma(n) = n-k where k is largest int s.t. 3**(k+1)+2k-1 <= 2n for hyperbolic functions
def sigma_hyper(n):
    k = -1
    sig = k
    done = 0
    while (3**(k+1) + 2*k - 1 <= 2*n):
        sig = k
        k += 1
    
    k = sig
    #print(n-sig)
    return n-k


#function for computing the cordic iteration for trig functions
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
    
    """ 
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
    """


#function for computing the cordic iteration for hyperbolic functions
def cordic_hyp_itr(ang, n):
    z = sp.posit32(ang)
    x = sp.posit32(1 / val_hyp_An(n))
    print(x)
    y = sp.posit32(0.0)
    di = 0
    arctanh_table = atanh_table(n)
   
    #iterate cordic algorithm
    for i in range(1,n+1):
        rot_ang = arctanh_table[2**(-sigma_hyper(i))]
        if z >= 0:
            di = 1
        else:
            di = -1
        
        x_prime = x + y * di * 2**(-sigma_hyper(i))
        y_prime = y + x * di * 2**(-sigma_hyper(i))
        z_prime = z - di * rot_ang
        
        #verification table - check that the iteration is correct
        print(i, 2.0**(-sigma_hyper(i)), rot_ang, z, rot_ang, z_prime)

        x = x_prime
        y = y_prime
        z = z_prime
    
    
    print("\nPosit representation:")
    print("cosh of %d (in degrees) = %.30f" %(ang, x))
    print("sinh of %d (in degrees) = %.30f" %(ang, y))
    print("tanh of %d (in degrees) = %.30f" %(ang, y/x))
    print("exp(%d) = %.30f" %(ang, x+y))
    print("ln(%d)  = %.30f" %(ang, 2*math.atanh((ang-1)/(ang+1))))

    print("\nMathlib representation:")
    print("cosh of %d (in degrees) = %.30f" %(ang, math.cosh(ang)))
    print("sinh of %d (in degrees) = %.30f" %(ang, math.sinh(ang)))
    print("tanh of %d (in degrees) = %.30f" %(ang, math.tanh(ang)))
    print("exp(%d) = %.30f" %(ang, math.exp(ang)))
    print("ln(%d) = %.30f" %(ang, math.log(ang)))

    print("\nMPFR representation:")
    print("cosh of %d (in degrees) = " %ang, bf.cosh(ang, bf.precision(PREC)))
    print("sinh of %d (in degrees) = " %ang, bf.sinh(ang, bf.precision(PREC)))
    print("tanh of %d (in degrees) = " %ang, bf.tanh(ang, bf.precision(PREC)))





##### Main Program #####

if __name__ == '__main__':
    """
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
    """

    #cordic_itr(30, 45)
    cordic_hyp_itr(0.4, 40)
    #sigma_hyper(1)


