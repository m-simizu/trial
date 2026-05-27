#include <assert.h>
#include <stdio.h>

#include "null_pointer.h"

int main(void) {
    int result = write_if_not_null(NULL, 99);
    assert(result == 0);
    printf("c_test_write_null: write_if_not_null(NULL, 99) = %d\n", result);
    return 0;
}
