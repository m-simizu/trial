#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "gcd.h"

int main(void) {
    uint64_t result = gcd(192, 270);
    assert(result == 6);
    printf("c_test_gcd_argument_order: gcd(192, 270) = %llu\n",
           (unsigned long long)result);
    return 0;
}
