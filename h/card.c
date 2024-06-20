#include <stdio.h>
#include "cs50.h"

int calculate(int n);

int main(void) {
    int n;
    do {
        n = get_int("Number: ");
    }
    while(n < 1);

    int counter = calculate(n);
    printf("%i", counter);


}

int calculate(int n) {
    int counter;
    for (int i = 1; n != 0; i++) {
        counter = n % 10; // 1234,5
    }
    return counter;
}