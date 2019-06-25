.RECIPEPREFIX +=

all: cordic_float cordic_posit

cordic_float: cordic_float.cpp
    #g++ -Wall -fdiagnostics-color=never -Werror -fsanitize=address -o cordic cordic_float.cpp 
    g++ -std=gnu++11 -Wall -fdiagnostics-color=never -Werror -o cordic_float cordic_float.cpp ../SoftPosit/build/Linux-x86_64-GCC/softposit.a -I../Softposit/sourceinclude -O2
   
cordic_posit: cordic_posit.cpp
    #g++ -Wall -fdiagnostics-color=never -Werror -fsanitize=address -o cordic cordic_float.cpp 
    g++ -std=gnu++11 -Wall -fdiagnostics-color=never -o cordic_posit cordic_posit.cpp ../SoftPosit/build/Linux-x86_64-GCC/softposit.a -I../Softposit/sourceinclude -O2

clean:
    rm -f cordic_posit
    rm -f cordic_float

