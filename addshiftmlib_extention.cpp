//Elementary functions to add to addshiftmlib.cpp

#include <math.h>
#include "../SoftPosit/source/include/softposit_cpp.h"
//#include "softposit_cpp.h"
#include <iostream>
#include <iomanip>
#include <vector>
#include <gmp.h>
#include <mpfr.h>
#include <stdio.h>
#include <fstream>

using namespace std;

//function to compute sigma(n) = n-k where k is largest int s.t. 3**(k+1)+2k-1 <= 2n for hyperbolic functions
int sigma(int n){
    int k = -1;
    int sig = k;
    int done = 0;
    while (pow(3,k+1) + pow(2,k) - 1 <= pow(2,n)){
        sig = k;
        k += 1;
    }
    k = sig;
    return n-k;
}

//function for computing sinh() - need to create a precomputed table of Kn/atanh
void posit_sinh(posit32 z, int n, posit32& sinh){
    posit32 x = k_hyp_p32[n]; // need to change precomputed numbers to fit hyperbolic;
    posit32 y = 0.0;
    posit32 di;
    
    //iterate cordic algorithm
    for(int i = 0; i < n; i++){
        posit32 pow2 = pow(2, -sigma(i));
        posit32 rot_ang = hyp_atan_table_p32[i]; //need to change table
        if(z >= 0){
            di = 1;
        }
        else{
            di = -1;
        }
        posit32 x_prime = x - y * di * pow2;
        posit32 y_prime = y + x * di * pow2;
        posit32 z_prime = z - di * rot_ang;
        
        x = x_prime;
        y = y_prime;
        z = z_prime;
    }
    
    sinh = y;
}



//function for computing cosh() - need to create a precomputed table of Kn/atanh
void posit_cosh(posit32 z, int n, posit32& cosh){
    posit32 x = k_hyp_p32[n]; // need to change precomputed numbers to fit hyperbolic;
    posit32 y = 0.0;
    posit32 di;
    
    //iterate cordic algorithm
    for(int i = 0; i < n; i++){
        posit32 pow2 = pow(2, -sigma(i));
        posit32 rot_ang = hyp_atan_table_p32[i]; //need to change table
        if(z >= 0){
            di = 1;
        }
        else{
            di = -1;
        }
        posit32 x_prime = x - y * di * pow2;
        posit32 y_prime = y + x * di * pow2;
        posit32 z_prime = z - di * rot_ang;
        
        x = x_prime;
        y = y_prime;
        z = z_prime;
    }
    
    cosh = x;
}


//function to compute sqrt() 
//  Parameters:
//
//    Input, posit32 X, the number whose square root is desired.
//    Input, int N, the number of iterations to take.
//    Output, double SQRT_CORDIC, the approximate square root of X.
void sqrt_cordic ( posit32 x, int n, posit32& sqrtx){
	posit32 poweroftwo;
	posit32 y;

	if ( x < 0.0 ){
		cout << "\n" << "SQRT_CORDIC - Fatal error!\n" << "  input < 0.\n";
		exit (1);
	}

	if ( x == 0.0 ){
		sqrtx = 0;
        return;
	}

	if ( x == 1.0 ){
		sqrtx = 1;
        return;
	}

	poweroftwo = 1.0;

	if ( x < 1.0 ){
		while ( x <= poweroftwo * poweroftwo ){
			poweroftwo = poweroftwo / 2.0;
		}
		y = poweroftwo;
	}

	else if ( 1.0 < x ){
		while ( poweroftwo * poweroftwo <= x ){
			poweroftwo = 2.0 * poweroftwo;
		}
		y = poweroftwo / 2.0;
	}

	for (int i = 1; i <= n; i++){
		poweroftwo = poweroftwo / 2.0;
		if ( ( y + poweroftwo ) * ( y + poweroftwo ) <= x ){
			y = y + poweroftwo;
		}
	}
	
	sqrtx = y;
}
