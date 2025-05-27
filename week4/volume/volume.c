// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int copy_header(FILE *input, FILE *output);
int copy_samples(FILE *input, FILE *output, float factor);

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    copy_header(input, output);

    // TODO: Read samples from input file and write updated data to output file
    copy_samples(input, output, factor);

    // Close files
    fclose(input);
    fclose(output);
}

int copy_header(FILE *input, FILE *output)
{
    // Read header from input file
    int8_t header[HEADER_SIZE];
    if (fread(header, HEADER_SIZE, 1, input) <= 0)
    {
        printf("Could not read header.\n");
        return 2;
    }

    // Write header to output file
    if (fwrite(header,  HEADER_SIZE, 1, output) <= 0)
    {
        printf("Could not write header.\n");
        return 3;
    }

    return 0;
}

int copy_samples(FILE *input, FILE *output, float factor)
{
    int16_t sample;
    while (fread(&sample, sizeof(int16_t), 1, input))
    {
        // Scale sample by factor
        sample = (int16_t)(sample * factor);

        if(fwrite(&sample, sizeof(int16_t), 1, output) <= 0)
        {
            printf("Could not write sample.\n");
            return 4;
        }
    }
    return 0;
}
