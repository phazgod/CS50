#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

const int block_size = 512;

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2) {
        printf("Usage: ./recover 'filename'\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "rb");
    if (card == NULL)
    {
        printf("Could not open.\n");
        return 2;
    }
    
    // Create a buffer for a block of data
    uint8_t buffer[512];

    bool found_jpg = false;
    int counter = 0;
    char filename[8];
    FILE *outptr = NULL;

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card)) {
        // Create JPEGs from the data
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) {
            found_jpg = true;
        }
        if (found_jpg == true) {
            if (counter != 0) {
                fclose(outptr);
            }
            sprintf(filename, "%03i.jpg", counter);
            outptr = fopen(filename, "wb");
            fwrite(buffer, 1, 512, outptr);
            found_jpg = false;
            counter++;
        }
        else if (counter != 0) {
            fwrite(buffer, 1, 512, outptr);
        }
    }
    fclose(outptr);
    fclose(card);
}