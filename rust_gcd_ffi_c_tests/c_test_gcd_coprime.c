#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "gcd.h"

int main(void) {
    uint64_t result = gcd(35, 64);
    assert(result == 1);
    printf("c_test_gcd_coprime: gcd(35, 64) = %llu\n",
           (unsigned long long)result);
    return 0;
}
