#include <stdio.h>
#include "cs50.h"

int main(void) {
    string words[2];
    words[0] = "HI!";
    words[1] = "BYE!";
    printf("%s%s%s\n", words[0], "\n", words[1]);
}