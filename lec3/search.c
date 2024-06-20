#include <stdio.h>
#include "cs50.h"
#include <string.h>

int main(void) {
    string strings[] = {"cat", "dog", "meow", "woof"};

    string s = get_string("Name: ");
    for (int i = 0; i < 4; i++) {
        if (strcmp(strings[i], s) == 0) {
            printf("Found\n");
            return 0;
        }
    }
    printf("Not Found\n");
    return 1;
}