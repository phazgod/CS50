#include <stdio.h>
#include <ctype.h> //isalpha, isblank
#include <string.h> //strlen
#include <math.h> //round
#include "cs50.h" //get_string, string

int letters = 0;
int spaces = 0;
int sentences = 0;

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void) {

    string text = get_string("Text: ");

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    
    float L = (float) letters / (float) words * 100;
    float S = (float) sentences / (float) words *100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int round_index = roundf(index);

    if (index < 1) {
        printf("Before Grade 1\n");
    }
    else if (index >= 1 && index <= 16) {
        printf("Grade %i\n", round_index);
    }
    else {
        printf("Grade 16+\n");
    }
}

int count_letters(string text)
{
    for (int i = 0, n = strlen(text); i < n; i++) {
        if (isalpha(text[i])) {
            letters++;
        }
    }
    return letters;
}
int count_words(string text)
{
    for (int i = 0, n = strlen(text); i < n; i++) {
        if (isblank(text[i])) {
            spaces++;
        }
    }
    int words = spaces + 1;
    return words;
}
int count_sentences(string text)
{
    for (int i = 0, n = strlen(text); i < n; i++) {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!') {
            sentences++;
        }
    }
    return sentences;
}