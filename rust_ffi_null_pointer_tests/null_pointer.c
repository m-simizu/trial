#include <stdio.h>

#include "null_pointer.h"

int read_or_default(const int *value, int default_value) {
    if (value == NULL) {
        return default_value;
    }

    return *value;
}

int write_if_not_null(int *target, int value) {
    if (target == NULL) {
        return 0;
    }

    *target = value;
    return 1;
}

#ifndef NULL_POINTER_NO_MAIN
int main(void) {
    int value = 42;
    int target = 0;

    printf("read_or_default(&value, -1): %d\n", read_or_default(&value, -1));
    printf("read_or_default(NULL, -1): %d\n", read_or_default(NULL, -1));
    printf("write_if_not_null(&target, 99): %d\n", write_if_not_null(&target, 99));
    printf("target: %d\n", target);
    printf("write_if_not_null(NULL, 99): %d\n", write_if_not_null(NULL, 99));

    return 0;
}
#endif
