//CORDIC algo to compute sine/cos/tan using IEEE floating point

#include <math.h>
#include <iostream>
#include <vector>
//#define M_PI
const float R_to_D = 180 / M_PI; //radians to degrees
const float D_to_R = M_PI / 180; //degrees to radians

using namespace std;

//function to return value of Ki
float val_Ki(int n){
    float Ki = 1 / sqrt(1 + pow(2,-2*n));
    return Ki;
}

//function to return value of An (cordic gain) 
float val_An(int n){
    float An = sqrt(2);
    for(int i = 1; i < n; i++){
        An = An * sqrt(1 + pow(2,-2*i));
    } 
    return An;
}

//function to create table of arctan values (tan:arctan)
void atan_table(float table[][2], int n){
    
    for(int i = 0; i < n+1; i++){
        table[i][0] = pow(2, -i);
        table[i][1] = atan(pow(2, -i)) * R_to_D;
    }
    return;    
}


//function for computing the cordic iteration
void cordic_itr(float ang, int n){
    float z = ang;
    float x = 1 / val_An(n);
    float y = 0;
    int di = 0;
    float arctan_table [50][2] = {};
    atan_table(arctan_table, n);

    //iterate cordic algorithm
    for(int i = 0; i < n+1; i++){
        float rot_ang = arctan_table[i][1];
        
        if(z >= 0){
            di = 1;
        }
        else{
            di = -1;
        }

        float x_prime = x - y * di * pow(2, -i);
        float y_prime = y + x * di * pow(2, -i);
        float z_prime = z - di * rot_ang;

        //verification table - to check if iteration is correct
        //printf("%d -- %f -- %f -- %f -- %f -- %f\n", i, pow(2, -i), rot_ang, z, rot_ang, z_prime);

        x = x_prime;
        y = y_prime;
        z = z_prime;
    }
    printf("\nFloat representation:\n");
    printf("cos of %f (in degrees) = %f\n", ang, x);
    printf("sin of %f (in degrees) = %f\n", ang, y);
    printf("tan of %f (in degrees) = %f\n", ang, y/x);
    
    //verify angle is correct
    printf("angle = %f \n", atan(y/x) * R_to_D);
    
    printf("\nMathlib representation:\n");
    printf("cos of %f (in degrees) = %f\n", ang, cos(M_PI/9));
    printf("sin of %f (in degrees) = %f\n", ang, sin(M_PI/9));
    printf("tan of %f (in degrees) = %f\n", ang, tan(M_PI/9));


    

}


//utility function to print 2d array
void print_2d(float table[][2], int n){
    for(int i = 0; i < n+1; i++){
        cout << table[i][0] << "    " << table[i][1] << endl;
    }
    return;
}

int main(){
    //cout << val_An(2) << endl;
    float table[50][2] = {};
    atan_table(table, 10);
    print_2d(table, 10);
    //cout << M_PI;

    cordic_itr(20, 40);

    return 0;

}
    

