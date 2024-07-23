#include <stdio.h>
#include "cs50.h"
#include <string.h>

int main(void) {
    string name = get_string("Name: ");
    int lenght = strlen(name);
    printf("%i\n", lenght);
}