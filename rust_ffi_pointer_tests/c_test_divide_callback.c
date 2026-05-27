#include <assert.h>
#include <stdio.h>

#include "arithmetic_callbacks.h"

int main(void) {
    int result = calculate(10, 5, divide);
    assert(result == 2);
    printf("c_test_divide_callback: calculate(10, 5, divide) = %d\n", result);
    return 0;
}
