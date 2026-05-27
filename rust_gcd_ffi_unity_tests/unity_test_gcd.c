#include <stdint.h>

#include "gcd.h"
#include "unity.h"

void setUp(void) {
}

void tearDown(void) {
}

static void test_gcd_common_factor(void) {
    TEST_ASSERT_EQUAL_UINT64(6, gcd(48, 18));
}

static void test_gcd_coprime_numbers(void) {
    TEST_ASSERT_EQUAL_UINT64(1, gcd(35, 64));
}

static void test_gcd_argument_order_does_not_matter(void) {
    TEST_ASSERT_EQUAL_UINT64(6, gcd(192, 270));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_gcd_common_factor);
    RUN_TEST(test_gcd_coprime_numbers);
    RUN_TEST(test_gcd_argument_order_does_not_matter);
    return UNITY_END();
}
