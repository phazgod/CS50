#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.0);
            // Update pixel values
            image[i][j].rgbtRed = image[i][j].rgbtBlue = image[i][j].rgbtGreen = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (sepiaRed > 255) {
                sepiaRed = 255;
            }
            if (sepiaBlue > 255) {
                sepiaBlue = 255;
            }
            if (sepiaGreen > 255) {
                sepiaGreen = 255;
            }
            // Update pixel with sepia values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
            {
                RGBTRIPLE buffer = image[i][j];
                image[i][j] = image[i][width - (j + 1)];
                image[i][width - (j + 1)] = buffer;
            }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            float sum_red = 0, sum_green = 0, sum_blue = 0, total_pixels = 0;
            for (int updated_i = i - 1; updated_i < i + 2; updated_i++) {
                for (int updated_j = j - 1; updated_j < j + 2; updated_j++) {
                    if (updated_i > 0 && updated_j > 0 && updated_i < height && updated_j < width) {
                        sum_red += image[updated_i][updated_j].rgbtRed;
                        sum_blue += image[updated_i][updated_j].rgbtBlue;
                        sum_green += image[updated_i][updated_j].rgbtGreen;
                        total_pixels++;
                    }
                }
            }
            copy[i][j].rgbtRed = round(sum_red / total_pixels);
            copy[i][j].rgbtBlue = round(sum_blue / total_pixels);
            copy[i][j].rgbtGreen = round(sum_green / total_pixels);
        }
    }
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            image[i][j] = copy[i][j];
        }
    }
}