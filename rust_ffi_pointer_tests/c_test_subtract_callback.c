#include <assert.h>
#include <stdio.h>

#include "arithmetic_callbacks.h"

int main(void) {
    int result = calculate(10, 5, subtract);
    assert(result == 5);
    printf("c_test_subtract_callback: calculate(10, 5, subtract) = %d\n", result);
    return 0;
}
