#include <assert.h>
#include <stdio.h>

#include "arithmetic_callbacks.h"

int main(void) {
    int result = calculate(10, 5, multiply);
    assert(result == 50);
    printf("c_test_multiply_callback: calculate(10, 5, multiply) = %d\n", result);
    return 0;
}
