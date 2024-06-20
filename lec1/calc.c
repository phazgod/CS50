#include <stdio.h>
#include "cs50.h"

int add(int first, int second);

int main(void) {
    int x = get_int("X: ");
    int y = get_int("Y: ");

    double z = (double) x / (double) y;
    printf("%.20f\n", z);
}