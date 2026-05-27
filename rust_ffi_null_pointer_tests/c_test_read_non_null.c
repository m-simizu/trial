#include <assert.h>
#include <stdio.h>

#include "null_pointer.h"

int main(void) {
    int value = 42;
    int result = read_or_default(&value, -1);
    assert(result == 42);
    printf("c_test_read_non_null: read_or_default(&value, -1) = %d\n", result);
    return 0;
}
