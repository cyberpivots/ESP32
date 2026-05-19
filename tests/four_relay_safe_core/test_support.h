#ifndef TEST_SUPPORT_H
#define TEST_SUPPORT_H

#include <stdbool.h>
#include <stdio.h>

static int failures = 0;

static void check(bool condition, const char *message)
{
    if (!condition) {
        fprintf(stderr, "FAIL: %s\n", message);
        ++failures;
    }
}

static int finish_tests(const char *name)
{
    if (failures != 0) {
        fprintf(stderr, "%s: %d failure(s)\n", name, failures);
        return 1;
    }
    printf("PASS: %s\n", name);
    return 0;
}

#endif
