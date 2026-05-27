#include <assert.h>
#include <stdio.h>

#include "arithmetic_callbacks.h"

int main(void) {
    int result = calculate(10, 5, add);
    assert(result == 15);
    printf("c_test_add_callback: calculate(10, 5, add) = %d\n", result);
    return 0;
}
