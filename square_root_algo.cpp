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
        if (num / 10 == 0){
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

    cout << output << endl;
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
        if (num / 10 == 0){
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
int main(int argc, char **argv){
    
    Rough_sqrt_est_posit(10);
    Rough_sqrt_est_float(10);
    return 0;
}
