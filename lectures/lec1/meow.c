#include "cs50.h"
#include <stdio.h>

int main(void) {
    int i = 0;
    for (i; i < 3; i++) {
        printf("meow\n");
    }
    printf("%i", i);
}