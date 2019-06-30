#CORDIC evaluation with posit

import math
import csv
import bitstring as bs
import softposit as sp
import bigfloat as bf
PREC = 100


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
    
    print(y)
    return y


def main():
    
    ang = 30

    p = cordic_itr(ang, 45)
    sin_mpfr = bf.sin(deg_to_rad(ang), bf.precision(PREC))
    sin_mathlib = math.sin(deg_to_rad(ang))
    bit1 = bs.BitArray(float=sin_mathlib, length=32)
    bit2 = bs.BitArray(float=0.5000000000000083, length=32)
    #0.50000000373
    #0.5000000000000083
    Bh = sp.posit32(0.50000000573)
    Bl = sp.posit32(0.50000000173)
    #blp = sp.castP16('0x0FF2')
    #print(blp)
    print("POSIT:")
    print("sin_mpfr: %.12f, p: %.12f, Bl: %.12f, Bh: %.12f" %(sin_mpfr, p, Bl, Bh))
    print("FLOAT:")
    print("sin_mathlib: ", bit1.bin)
    print("sin_float: ", bit2.bin)
    print("sin_mathlib: %.12E, p: %.12E, Bl: %.12E, Bh: %.12E" %(sin_mathlib, p, Bl, Bh))
    print(sin_mpfr, p, Bl, Bh)
    p.toBinaryFormatted()
    Bl.toBinaryFormatted()
    Bh.toBinaryFormatted()
    
main()
