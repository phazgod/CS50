#include <stdio.h>
#include "cs50.h"

int main(void) {
    int n;
    do {
        n = get_int("Height: ");
    }
    while (n < 1);

    for (int i = 0; i < n; i++) {
        for (int k = n - i; k != 1; k--) {
            printf(" ");
        }
        for (int j = 0; j <= i; j++) {
            printf("#");
        }
        printf(" ");
        for (int p = 0; p <= i; p++) {
            printf("#");
        }
        printf("\n");
    }
}