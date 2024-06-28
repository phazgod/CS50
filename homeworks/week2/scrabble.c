#include <stdio.h>
#include "cs50.h"
#include <string.h>
#include <ctype.h>

const int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void) {

    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    int sum1 = compute_score(word1);
    int sum2 = compute_score(word2);

    if (sum1 > sum2) {
        printf("Player 1 WIN!\n");
    }
    else if (sum1 < sum2) {
        printf("Player 2 WIN!\n");
    }
    else {
        printf("Tie!\n");
    }
    printf("Score1: %i\n", sum1);
    printf("Score2: %i\n", sum2);
}

int compute_score(string word) {
    int sum = 0;
    for (int i = 0, n = strlen(word); i < n; i++) {
        if (isupper(word[i])) {
            sum += POINTS[word[i] - 'A'];
        }
        else if (islower(word[i])) {
            sum += POINTS[word[i] - 'a'];
        }
        }
    return sum;
}