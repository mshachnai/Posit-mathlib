//implementation of CORDIC with float

#include <cmath>
#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <ctime>
#include <fstream>

using namespace std;


float angle_shift ( float alpha, float beta )

	//****************************************************************************80
	//
	//  Purpose:
	//
	//    ANGLE_SHIFT shifts angle ALPHA to lie between BETA and BETA+2PI.
	//
	//  Discussion:
	//
	//    The input angle ALPHA is shifted by multiples of 2 * PI to lie
	//    between BETA and BETA+2*PI.
	//
	//    The resulting angle GAMMA has all the same trigonometric function
	//    values as ALPHA.
	//
	//  Licensing:
	//
	//    This code is distributed under the GNU LGPL license. 
	//
	//  Modified:
	//
	//    14 June 2007
	//
	//  Author:
	//
	//    John Burkardt
	//
	//  Parameters:
	//
	//    Input, float ALPHA, the angle to be shifted.
	//
	//    Input, float BETA, defines the lower endpoint of
	//    the angle range.
	//
	//    Output, float ANGLE_SHIFT, the shifted angle.
	//
{
	float gamma;
	float pi = 3.141592653589793;

	if ( alpha < beta )
	{
		gamma = beta - fmod ( beta - alpha, 2.0 * pi ) + 2.0 * pi;
	}
	else
	{
		gamma = beta + fmod ( alpha - beta, 2.0 * pi );
	}

	return gamma;
}

int i4_min ( int i1, int i2 )

    //****************************************************************************80
    //
    //  Purpose:
    //
    //    I4_MIN returns the minimum of two I4's.
    //
    //  Licensing:
    //
    //    This code is distributed under the GNU LGPL license. 
    //
    //  Modified:
    //
    //    13 October 1998
    //
    //  Author:
    //
    //    John Burkardt
    //
    //  Parameters:
    //
    //    Input, int I1, I2, two integers to be compared.
    //
    //    Output, int I4_MIN, the smaller of I1 and I2.
    //
{
    int value;

    if ( i1 < i2 )
    {
        value = i1;
    }
    else
    {
        value = i2;
    }
    return value;
}

void cossin_cordic ( float beta, int n, float &c, float &s, ofstream& file)

	//****************************************************************************80
	//
	//  Purpose:
	//
	//    COSSIN_CORDIC returns the sine and cosine of an angle by the CORDIC method.
	//
	//  Licensing:
	//
	//    This code is distributed under the GNU LGPL license. 
	//
	//  Modified:
	//
	//    14 June 2007
	//
	//  Author:
	//
	//    Based on MATLAB code in a Wikipedia article.
	//    C++ version by John Burkardt
	//
	//  Parameters:
	//
	//    Input, float BETA, the angle (in radians).
	//
	//    Input, int N, the number of iterations to take.
	//    A value of 10 is low.  Good accuracy is achieved with 20 or more
	//    iterations.
	//
	//    Output, float &C, &S, the cosine and sine of the angle.
	//
	//  Local Parameters:
	//
	//    Local, float ANGLES(60) = arctan ( (1/2)^(0:59) );
	//
	//    Local, float KPROD(33).  KPROD(j) = product ( 0 <= i <= j ) K(i)
	//    where K(i) = 1 / sqrt ( 1 + (1/2)^(2i) ).
	//
{
# define ANGLES_LENGTH 60
# define KPROD_LENGTH 33

	float angle;
	float angles[ANGLES_LENGTH] = {
		7.8539816339744830962E-01, 
		4.6364760900080611621E-01, 
		2.4497866312686415417E-01, 
		1.2435499454676143503E-01, 
		6.2418809995957348474E-02, 
		3.1239833430268276254E-02, 
		1.5623728620476830803E-02, 
		7.8123410601011112965E-03, 
		3.9062301319669718276E-03, 
		1.9531225164788186851E-03, 
		9.7656218955931943040E-04, 
		4.8828121119489827547E-04, 
		2.4414062014936176402E-04, 
		1.2207031189367020424E-04, 
		6.1035156174208775022E-05, 
		3.0517578115526096862E-05, 
		1.5258789061315762107E-05, 
		7.6293945311019702634E-06, 
		3.8146972656064962829E-06, 
		1.9073486328101870354E-06, 
		9.5367431640596087942E-07, 
		4.7683715820308885993E-07, 
		2.3841857910155798249E-07, 
		1.1920928955078068531E-07, 
		5.9604644775390554414E-08, 
		2.9802322387695303677E-08, 
		1.4901161193847655147E-08, 
		7.4505805969238279871E-09, 
		3.7252902984619140453E-09, 
		1.8626451492309570291E-09, 
		9.3132257461547851536E-10, 
		4.6566128730773925778E-10, 
		2.3283064365386962890E-10, 
		1.1641532182693481445E-10, 
		5.8207660913467407226E-11, 
		2.9103830456733703613E-11, 
		1.4551915228366851807E-11, 
		7.2759576141834259033E-12, 
		3.6379788070917129517E-12, 
		1.8189894035458564758E-12, 
		9.0949470177292823792E-13, 
		4.5474735088646411896E-13, 
		2.2737367544323205948E-13, 
		1.1368683772161602974E-13, 
		5.6843418860808014870E-14, 
		2.8421709430404007435E-14, 
		1.4210854715202003717E-14, 
		7.1054273576010018587E-15, 
		3.5527136788005009294E-15, 
		1.7763568394002504647E-15, 
		8.8817841970012523234E-16, 
		4.4408920985006261617E-16, 
		2.2204460492503130808E-16, 
		1.1102230246251565404E-16, 
		5.5511151231257827021E-17, 
		2.7755575615628913511E-17, 
		1.3877787807814456755E-17, 
		6.9388939039072283776E-18, 
		3.4694469519536141888E-18, 
		1.7347234759768070944E-18 };
	float c2;
	float factor;
	int j;
	float kprod[KPROD_LENGTH] = {
		0.70710678118654752440, 
		0.63245553203367586640, 
		0.61357199107789634961, 
		0.60883391251775242102, 
		0.60764825625616820093, 
		0.60735177014129595905, 
		0.60727764409352599905, 
		0.60725911229889273006, 
		0.60725447933256232972, 
		0.60725332108987516334, 
		0.60725303152913433540, 
		0.60725295913894481363, 
		0.60725294104139716351, 
		0.60725293651701023413, 
		0.60725293538591350073, 
		0.60725293510313931731, 
		0.60725293503244577146, 
		0.60725293501477238499, 
		0.60725293501035403837, 
		0.60725293500924945172, 
		0.60725293500897330506, 
		0.60725293500890426839, 
		0.60725293500888700922, 
		0.60725293500888269443, 
		0.60725293500888161574, 
		0.60725293500888134606, 
		0.60725293500888127864, 
		0.60725293500888126179, 
		0.60725293500888125757, 
		0.60725293500888125652, 
		0.60725293500888125626, 
		0.60725293500888125619, 
		0.60725293500888125617 };
	float pi = 3.141592653589793;
	float poweroftwo;
	float s2;
	float sigma;
	float sign_factor;
	float theta;
	//
	//  Shift angle to interval [-pi,pi].
	//
	theta = angle_shift ( beta, -pi );
	//
	//  Shift angle to interval [-pi/2,pi/2] and account for signs.
	//
	if ( theta < - 0.5 * pi )
	{
		theta = theta + pi;
		sign_factor = -1.0;
	}
	else if ( 0.5 * pi < theta )
	{
		theta = theta - pi;
		sign_factor = -1.0;
	}
	else
	{
		sign_factor = +1.0;
	}
	//
	//  Initialize loop variables:
	//
	c = 1.0;
	s = 0.0;

	poweroftwo = 1.0;
	angle = angles[0];
	//
	//  Iterations
	//
	for ( j = 1; j <= n; j++ )
	{
		if ( theta < 0.0 )
		{
			sigma = -1.0;
		}
		else
		{
			sigma = 1.0;
		}

		factor = sigma * poweroftwo;

		c2 =          c - factor * s;
		s2 = factor * c +          s;

		c = c2;
		s = s2;
		//
		//  Update the remaining angle.
		//
		theta = theta - sigma * angle;

		poweroftwo = poweroftwo / 2.0;
		//
		//  Update the angle from table, or eventually by just dividing by two.
		//
		if ( ANGLES_LENGTH < j + 1 )
		{
			angle = angle / 2.0;
		}
		else
		{
			angle = angles[j];
		}
	}
	//
	//  Adjust length of output vector to be [cos(beta), sin(beta)]
	//
	//  KPROD is essentially constant after a certain point, so if N is
	//  large, just take the last available value.
	//
	if ( 0 < n )
	{
		c = c * kprod [ i4_min ( n, KPROD_LENGTH ) - 1 ];
		s = s * kprod [ i4_min ( n, KPROD_LENGTH ) - 1 ];
	}
	//
	//  Adjust for possible sign change because angle was originally
	//  not in quadrant 1 or 4.
	//
	c = sign_factor * c;
	s = sign_factor * s;

    float x = c;
    float y = s;
    //mathlib trig functions
    double sin_mathlib = sin(beta);
    double cos_mathlib = cos(beta);
    double tan_mathlib = tan(beta);
    double s_err = (sin_mathlib - y) / sin_mathlib;
    double c_err = (cos_mathlib - x) / cos_mathlib;
    double t_err = (tan_mathlib - y/x) / tan_mathlib;


    //output results to csv file
    file << int(beta) << scientific << ',' << y << ',' << sin_mathlib << ',' << s_err 
        << ',' << x << ','<< cos_mathlib << ',' << c_err << ',' << y/x << ',' 
        << tan_mathlib << ',' << t_err << '\n'; 

	return;
# undef ANGLES_LENGTH
# undef KPROD_LENGTH
}

int main(){
    float x;
    float y; 

    //create output file
    ofstream file;
    file.open("float_sec_imple.csv");
    file << scientific << "Angle, Float-sin, Mathlib-sin, Error, Float-cos, Mathlib-cos, Error, Float-tan, Mathlib-tan, Error \n"; 

    for(int i = 0; i < 361; i++){
        cossin_cordic(i * M_PI/180.0, 40, x, y, file);
    }

}

