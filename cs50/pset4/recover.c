#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

// FAT File system block size is usually 512
#define BLOCK_SIZE 512

// Let's provide ourself with a BYTE typedef
typedef uint8_t BYTE;

bool can_be_jpeg(int j, int p, int e, int g)
{
    // This could be done in one if-statement
    // For readability and tweaking purposes, I prefer to keep it like this.
    if (j != 0xff)
    {
        return 0;
    }
    if (p != 0xd8)
    {
        return 0;
    }
    if (e != 0xff)
    {
        return 0;
    }
    if ((g & 0xf0) != 0xe0)
    {
        return 0;
    }

    // If none of these checks return false, it's probably a jpeg
    return 1;
}

int main(int argc, char *argv[])
{
    // Check for the right amount of arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open the file provided in the argument
    FILE *file = fopen(argv[1], "r");

    // fopen returns NULL if file cannot be read. As such, use this to handle as exception.
    if (file == NULL)
    {
        printf("Could not read file. Try again with a different file.\n");
        return 1;
    }

    // Let's make space for a buffer
    BYTE buffer[512];

    // Set a counter, that indicates how many images we have found, so we can change names later.
    int c = 0;

    // Create a new image
    FILE *output = NULL;

    // Loop until EOF
    while (fread(buffer, BLOCK_SIZE, 1, file) == 1)
    {
        if (can_be_jpeg(buffer[0], buffer[1], buffer[2], buffer[3]) == 1)
        {
            // Close out the outputfile, if it already exists.
            if (output != NULL)
            {
                fclose(output);
                c++;
            }

            // Create filename n, that has 000.jpeg as format.
            // Open the file and write the BLOCK_SIZE to the file.
            char n[8];
            sprintf(n, "%03i.jpg", c);
            output = fopen(n, "w");
        }

        if (output != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, output);
        }
    }

    // After all this, close the last image if exists
    if (output != NULL)
    {
        fclose(output);
    }

    // Close the input file
    fclose(file);

    return 0;
}
