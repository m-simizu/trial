#ifndef NULL_POINTER_H
#define NULL_POINTER_H

#include <stddef.h>

int read_or_default(const int *value, int default_value);
int write_if_not_null(int *target, int value);

#endif
