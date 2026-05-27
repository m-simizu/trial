#include <stdio.h>

#include "arithmetic_callbacks.h"

// コールバック関数として呼び出される四則演算関数
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }
int multiply(int a, int b) { return a * b; }
int divide(int a, int b) { return a / b; }

// 関数ポインタを引数にとる計算実行部
int calculate(int x, int y, ArithmeticCallback callback) {
    return callback(x, y);
}

#ifndef ARITHMETIC_CALLBACKS_NO_MAIN
int main(void) {
    int a = 10;
    int b = 5;

    printf("add: %d\n", calculate(a, b, add));
    printf("subtract: %d\n", calculate(a, b, subtract));
    printf("multiply: %d\n", calculate(a, b, multiply));
    printf("divide: %d\n", calculate(a, b, divide));

    return 0;
}
#endif
