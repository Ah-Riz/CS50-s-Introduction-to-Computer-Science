#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <input file>\n", argv[0]);
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        perror("Could not open input file");
        return 2;
    }

    BYTE buffer[BLOCK_SIZE];
    int file_count = 0;
    FILE *output = NULL;

    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, input) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (output != NULL)
            {
                fclose(output);
            }
            char filename[8];
            sprintf(filename, "%03d.jpg", file_count++);
            output = fopen(filename, "w");
            if (output == NULL)
            {
                perror("Could not create output file");
                fclose(input);
                return 3;
            }
        }

        if (output != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, output);
        }
    }

    if (output != NULL)
    {
        fclose(output);
    }
    
    fclose(input);
    return 0;
}