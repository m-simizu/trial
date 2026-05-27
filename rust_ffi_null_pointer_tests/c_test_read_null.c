#include <assert.h>
#include <stdio.h>

#include "null_pointer.h"

int main(void) {
    int result = read_or_default(NULL, -1);
    assert(result == -1);
    printf("c_test_read_null: read_or_default(NULL, -1) = %d\n", result);
    return 0;
}
