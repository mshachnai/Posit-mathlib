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



posit32 exp_cordic ( posit32 x, int n ){
# define A_LENGTH 25


//change precomputed table to posits
  double a[A_LENGTH] = { 
    1.648721270700128, 
    1.284025416687742, 
    1.133148453066826, 
    1.064494458917859, 
    1.031743407499103, 
    1.015747708586686, 
    1.007843097206488, 
    1.003913889338348, 
    1.001955033591003, 
    1.000977039492417, 
    1.000488400478694, 
    1.000244170429748, 
    1.000122077763384, 
    1.000061037018933, 
    1.000030518043791, 
    1.0000152589054785, 
    1.0000076294236351, 
    1.0000038147045416, 
    1.0000019073504518, 
    1.0000009536747712, 
    1.0000004768372719, 
    1.0000002384186075, 
    1.0000001192092967, 
    1.0000000596046466, 
    1.0000000298023228 };
  posit32 ai;
  posit32 e = 2.718281828459045;
  posit32 fx;
  int i;
  posit32 poweroftwo;
  posit32 *w;
  int x_int;
  posit32 z;

  x_int = ( int ) ( floor ( x ) );
//
//  Determine the weights.
//
  poweroftwo = 0.5;
  z = x - ( posit32 ) ( x_int );

  w = new posit32[n];

  for ( i = 0; i < n; i++ )
  {
    w[i] = 0.0;
    if ( poweroftwo < z )
    {
      w[i] = 1.0;;
      z = z - poweroftwo;
    }
    poweroftwo = poweroftwo / 2.0;
  }
//
//  Calculate products.
//
  fx = 1.0;

  for ( i = 0; i < n; i++ )
  {
    if ( i < A_LENGTH )
    {
      ai = a[i];
    }
    else
    {
      ai = 1.0 + ( ai - 1.0 ) / 2.0;
    }

    if ( 0.0 < w[i] )
    {
      fx = fx * ai;
    }
  }
//
//  Perform residual multiplication.
//
  fx = fx                     
    * ( 1.0 + z           
    * ( 1.0 + z / 2.0 
    * ( 1.0 + z / 3.0 
    * ( 1.0 + z / 4.0 ))));
//
//  Account for factor EXP(X_INT).
//
  if ( x_int < 0 )
  {
    for ( i = 1; i <= -x_int; i++ )
    {
      fx = fx / e;
    }
  }
  else
  {
    for ( i = 1; i <= x_int; i++ )
    {
      fx = fx * e;
    }
  }

  delete [] w;

  return fx;
# undef A_LENGTH
}
