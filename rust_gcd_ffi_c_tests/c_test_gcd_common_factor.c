#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "gcd.h"

int main(void) {
    uint64_t result = gcd(48, 18);
    assert(result == 6);
    printf("c_test_gcd_common_factor: gcd(48, 18) = %llu\n",
           (unsigned long long)result);
    return 0;
}
