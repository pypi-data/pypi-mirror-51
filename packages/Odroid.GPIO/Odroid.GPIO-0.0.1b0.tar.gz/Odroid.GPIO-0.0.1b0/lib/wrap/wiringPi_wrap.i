%module GPIO

%{
    #include <wiringPi.h>
%}

extern		int  wiringPiSetup	(void);
extern		void pinMode		(int pin, int mode);
extern		int  digitalRead	(int pin);
extern		void digitalWrite	(int pin, int value);