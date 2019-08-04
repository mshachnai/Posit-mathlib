//Various algorithms for calculating sqrt function with posit and fp

#include <math.h>
#include "../SoftPosit/source/include/softposit_cpp.h"
#include <iostream>
#include <iomanip>
#include <vector>
#include <gmp.h>
#include <mpfr.h>
#include <stdio.h>
#include <fstream>

using namespace std;

//Rough estimation of sqrt function - posit 
posit32 Rough_sqrt_est_posit(int S){
    posit32 a = S;
    posit32 output = 0;
    int num = S;
    int i = 0;
    int exp = 0;

    for (i = 0; i < 100; i++){
        if (round(num) / 10 == 0){
            i++;
            break;
        }

        else{
            num = num / 10;
        }
    }
    
    exp = i;
    if (exp % 2 != 0){
        exp--;
    }

    for (i = 0; i < exp; i++){
        a = a / 10;
    }
    
    //fix decimal place of a if smaller than 1
    if (a < 1){
        exp -= 2;
        a *= 100;
    }
    cout << a << " " << exp << endl;

    if (a < 10){
        output = 2 * pow(10, exp/2);
    }
    else{
        output = 6 * pow(10, exp/2);
    }

    cout << "sqrt estimation = " << output << endl;
    return output;

}

//Rough estimation of sqrt function - float 
float Rough_sqrt_est_float(int S){
    float a = S;
    float output = 0;
    int num = S;
    int i = 0;
    int exp = 0;

    for (i = 0; i < 100; i++){
        if (int(num) / 10 == 0){
            i++;
            break;
        }

        else{
            num = num / 10;
        }
    }
    
    exp = i;
    if (exp % 2 != 0){
        exp--;
    }

    for (i = 0; i < exp; i++){
        a = a / 10;
    }
    
    //fix decimal place of a if smaller than 1
    if (a < 1){
        exp -= 2;
        a *= 100;
    }
    //cout << a << " " << exp << endl;

    if (a < 10){
        output = 2 * pow(10, exp/2);
    }
    else{
        output = 6 * pow(10, exp/2);
    }

    //cout << output << endl;
    return output;

}

posit32 Babylonian_sqrt_posit(int S){
    posit32 x = Rough_sqrt_est_posit(S);
    posit32 x_prime = 0;
    int i = 0;
    int iter = 5;

    for (i = 0; i < iter; i++){
        x_prime = 0.5 * (x + (S / x));
        cout << x << " " << x_prime << endl;
        x = x_prime;
    }

    return x_prime;
}

float Babylonian_sqrt_float(int S){
    float x = Rough_sqrt_est_float(S);
    float x_prime = 0;
    int i = 0;
    int iter = 5;

    for (i = 0; i < iter; i++){
        x_prime = 0.5 * (x + (S / x));
        //cout << x << " " << x_prime << endl;
        x = x_prime;
    }

    return x_prime;
}


posit32 Bakhshali_sqrt_posit(int S){
    posit32 x = Rough_sqrt_est_posit(S);
    posit32 x_prime = 0;
    posit32 a = 0;
    posit32 b = 0;
    int i = 0;
    int iter = 5;

    for (i = 0; i < iter; i++){
        a = (S - (x*x)) / (2 * x);
        b = x + a;
        x_prime = b - (a*a) / (2 * b); 
        //cout << a << " " << b << " " << x_prime << endl;
        x = x_prime;
    }

    return x_prime;
}

float Bakhshali_sqrt_float(int S){
    float x = Rough_sqrt_est_float(S);
    float x_prime = 0;
    float a = 0;
    float b = 0;
    int i = 0;
    int iter = 5;

    for (i = 0; i < iter; i++){
        a = (S - (x*x)) / (2 * x);
        b = x + a;
        x_prime = b - (a*a) / (2 * b); 
        cout << a << " " << b << " " << x_prime << endl;
        x = x_prime;
    }

    return x_prime;
}


int main(int argc, char **argv){
    
    //Rough_sqrt_est_posit(125348);
    //Rough_sqrt_est_float(10);
    
    //Babylonian_sqrt_posit(125348);
    //Babylonian_sqrt_float(125348);

    //Bakhshali_sqrt_posit(125348);
    //Bakhshali_sqrt_float(125348);
    return 0;
}
