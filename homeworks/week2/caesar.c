#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "cs50.h"
#include <stdlib.h>

int main(int argc, string argv[]) {
    if (argc != 2) {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int counter = 0;
    int n = strlen(argv[1]);
    for (int i = 0; i < n; i++) {
        if (isdigit(argv[1][i])) {
            counter++;
        }
    }
    if (counter != n) {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int key = atoi(argv[1]);

    string text = get_string("plaintext: ");
    int size = strlen(text);
    int array[size];
    printf("cyphertext: ");
    for (int i = 0; i < size; i++) {
        if (isalpha(text[i]) && islower(text[i])) {
            array[i] = text[i] - 97;
            array[i] = (array[i] + key) % 26;
            printf("%c", array[i] + 97);
        }
        else if (isalpha(text[i]) && isupper(text[i])) {
            array[i] = text[i] - 65;
            array[i] = (array[i] + key) % 26;
            printf("%c", array[i] + 65);
        }
        else if (ispunct(text[i]) || isdigit(text[i])) {
            array[i] = text[i];
            printf("%c", array[i]);
        }
        else {
            array[i] = text[i];
            printf("%c", array[i]);
        }
    }
}