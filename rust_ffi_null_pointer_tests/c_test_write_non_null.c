#include <assert.h>
#include <stdio.h>

#include "null_pointer.h"

int main(void) {
    int target = 0;
    int result = write_if_not_null(&target, 99);
    assert(result == 1);
    assert(target == 99);
    printf("c_test_write_non_null: write_if_not_null(&target, 99) = %d, target = %d\n",
           result,
           target);
    return 0;
}
