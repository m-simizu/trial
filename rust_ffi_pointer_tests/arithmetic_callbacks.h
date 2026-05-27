#ifndef ARITHMETIC_CALLBACKS_H
#define ARITHMETIC_CALLBACKS_H

typedef int (*ArithmeticCallback)(int, int);

int add(int a, int b);
int subtract(int a, int b);
int multiply(int a, int b);
int divide(int a, int b);
int calculate(int x, int y, ArithmeticCallback callback);

#endif
