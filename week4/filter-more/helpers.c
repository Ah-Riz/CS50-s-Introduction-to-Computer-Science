#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            // float average = ((image[i][j].rgbtRed * 0.299) + (image[i][j].rgbtGreen *0.587) + (image[i][j].rgbtBlue * 0.114));
            float average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            int average_int = round(average);
            image[i][j].rgbtRed = average_int;
            image[i][j].rgbtGreen = average_int;
            image[i][j].rgbtBlue = average_int;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width / 2; j++)
        {
            // Swap pixels
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            int red_sum = 0, green_sum = 0, blue_sum = 0;
            int count = 0;

            // Check surrounding pixels
            for(int di = -1; di <= 1; di++)
            {
                for(int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // Ensure within bounds
                    if(ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        red_sum += image[ni][nj].rgbtRed;
                        green_sum += image[ni][nj].rgbtGreen;
                        blue_sum += image[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }

            // Calculate average
            temp[i][j].rgbtRed = round((float)red_sum / count);
            temp[i][j].rgbtGreen = round((float)green_sum / count);
            temp[i][j].rgbtBlue = round((float)blue_sum / count);
        }
    }
    // Copy temp array to original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    RGBTRIPLE temp[height][width];
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            int red_x = 0, green_x = 0, blue_x = 0;
            int red_y = 0, green_y = 0, blue_y = 0;

            // Apply Sobel operator
            for(int di = -1; di <= 1; di++)
            {
                for(int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // Ensure within bounds
                    if(ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        red_x += image[ni][nj].rgbtRed * Gx[di + 1][dj + 1];
                        green_x += image[ni][nj].rgbtGreen * Gx[di + 1][dj + 1];
                        blue_x += image[ni][nj].rgbtBlue * Gx[di + 1][dj + 1];

                        red_y += image[ni][nj].rgbtRed * Gy[di + 1][dj + 1];
                        green_y += image[ni][nj].rgbtGreen * Gy[di + 1][dj + 1];
                        blue_y += image[ni][nj].rgbtBlue * Gy[di + 1][dj + 1];
                    }
                }
            }

            // Calculate final color values
            int red_final = round(sqrt(red_x * red_x + red_y * red_y));
            int green_final = round(sqrt(green_x * green_x + green_y * green_y));
            int blue_final = round(sqrt(blue_x * blue_x + blue_y * blue_y));

            // Clamp values to [0, 255]
            temp[i][j].rgbtRed = fmin(255, red_final);
            temp[i][j].rgbtGreen = fmin(255, green_final);
            temp[i][j].rgbtBlue = fmin(255, blue_final);
        }
    }

    // Copy temp array back to original image  
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}
