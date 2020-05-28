#include "helpers.h"
#include <math.h>

// Check if a value exceeds the maximum number supported in rgb (255)
// This keeps code in one place, so it's easier to maintain in the future
int check_for_max(int input)
{
    if (input > 255)
    {
        return 255;
    }
    return input;
}

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // First loop through the rows
    for (int h = 0; h < height; h++)
    {
        // Then, loop through the columns
        for (int w = 0; w < width; w++)
        {
            // The easiest way to convert to grayscale is by using a lineair approach
            // Which is to say, divide the total by 3.
            // First, let's get the numbers we need, but pass them as floats to prevent integer division.
            float r = image[h][w].rgbtRed;
            float g = image[h][w].rgbtGreen;
            float b = image[h][w].rgbtBlue;

            // Calculate the total by 3 and round it to the nearest number.
            int c = round((r + b + g) / 3);

            // Write this new number to the RGBTRIPLE
            image[h][w].rgbtRed = c;
            image[h][w].rgbtGreen = c;
            image[h][w].rgbtBlue = c;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // First loop through the rows
    for (int h = 0; h < height; h++)
    {
        // Then, loop through the columns
        for (int w = 0; w < width; w++)
        {
            // With the provided sepia function, convert to sepia
            // First, let's initialize the values as float, to prevent integer division.
            float r = image[h][w].rgbtRed;
            float g = image[h][w].rgbtGreen;
            float b = image[h][w].rgbtBlue;

            // Calculate and set the sepia values with provided formula
            image[h][w].rgbtRed = check_for_max(round(.393 * r + .769 * g + .189 * b));
            image[h][w].rgbtGreen = check_for_max(round(.349 * r + .686 * g + .168 * b));
            image[h][w].rgbtBlue = check_for_max(round(.272 * r + .534 * g + .131 * b));
        }
    }



    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Make sure we have an even amount of columns
    // So that we do not have to mirror the column in the middle

    // Then, loop through the rows
    for (int h = 0; h < height; h++)
    {
        // And loop through the columns.
        for (int w = 0; w < (round(0.5 * width)); w++)
        {
            // Create a temporary RGBTriple and set the contents of the current pixel to temp
            RGBTRIPLE temp = image[h][w];

            // Then, go set the pixel to the reflected pixel
            image[h][w] = image[h][width - w - 1];

            // Lastly, set temp to the reflected pixel
            image[h][width - w - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Before we start work on manipulating the image, we should make a new copy
    RGBTRIPLE copy[height][width];

    // Now, iterate over the rows and columns, like previously.
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            // Set a counter and set float for rgb, to make sure we won't get integer division.
            int c = 0;
            float r = 0;
            float b = 0;
            float g = 0;

            // Set local vertical positioning, to iterate from one line up to one line down
            for (int vp = -1; vp < 2; vp++)
            {
                // Skip over heights outside image boundaries
                if (h + vp < 0 || h + vp > height - 1)
                {
                    continue;
                }
                
                // Set local horizontal positioning, to iterate from left to right
                for (int hp = -1; hp < 2; hp++)
                {
                    // Skip over widths outside image boundaries
                    if (w + hp < 0 || w + hp > width - 1)
                    {
                        continue;
                    }
                    
                    // Now, writes these values to the temporary value
                    r += image[h + vp][w + hp].rgbtRed;
                    g += image[h + vp][w + hp].rgbtGreen;
                    b += image[h + vp][w + hp].rgbtBlue;
                    c++;
                }
            }
            
            // Write the rounded average values to the copy
            copy[h][w].rgbtRed = round(r / c);
            copy[h][w].rgbtGreen = round(g / c);
            copy[h][w].rgbtBlue = round(b / c);
        }
    }
    
    // Set the image to the copy
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w] = copy[h][w];
        }
    }

    return;
}
